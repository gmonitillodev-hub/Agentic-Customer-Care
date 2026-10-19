# Design Decisions

Log of technical decisions. Newest entries at the bottom.

## D-001 — Session entities: storage and injection into the agent

**Context.** The `EntityExtractorAgent` extracts user data (name, surname, email, address) from the conversation. The main agent must know these values on every turn, without re-asking the user.

### Storage: `dict[str, SessionEntity]`

- `CustomerCareAgent.session_data: dict[str, SessionEntity]`, keyed by `sessionId`.
- O(1) lookup, and it replaces the separate `active_sessions: list[str]` (a session exists if its key exists).
- `_check_session` returns the given id if known, otherwise generates a new uuid and creates an empty `SessionEntity`.
- `SessionEntity.sessionId` is typed `str` (it was wrongly typed with the `uuid` module).

### Update: `SessionEntity.merge_data` + background extraction

- The extraction runs in an `@after_agent` middleware (`build_entities_updater`), **after** the main agent finished.
- The hook is `async` and does **not** await the extraction: it schedules it with `asyncio.create_task` and returns, so `ainvoke()` completes and the answer is returned without waiting for the extractor.
- Inside the task, `await asyncio.to_thread(extractor.invoke, state)` runs the sync, blocking extractor in a worker thread, keeping the event loop free. No `ainvoke` is needed on the extractor.
- The `structured_response` of the extractor is deep-merged into `SessionEntity.data` (`merge_data`).
- Nested models (`UserInfo`, `AddressInfo`) are merged recursively.
- A `None` value never overwrites an existing one, so data accumulates across turns.
- `interact` is `async` and uses `agent.ainvoke`. Returning session data to the user is not a requirement; the returned `session_data.data` is only informational and may not yet include the current turn.
- Calling a coroutine without `await` does not run it; `create_task` is what schedules it without waiting.

### Injection: `context_schema` + `@dynamic_prompt` middleware

- `create_agent(..., context_schema=SessionEntity, middleware=[prompt_middleware, entities_updater])`.
- `interact` calls `agent.ainvoke(..., context=session_data)`; the same `SessionEntity` object is mutated by the background task.
- The `entities_prompt` middleware (`build_prompt_enrichment`) reads `request.runtime.context` and returns the **full** system prompt: `CC_AGENT_SYSTEM_PROMPT` + known user data.
- `system_prompt=` was removed from `create_agent`: a `dynamic_prompt` replaces it, so the base prompt lives in the middleware.
- With no context, only the base prompt is returned.

**Why this and not the alternatives**

| Option | Outcome |
|---|---|
| `context_schema` + `dynamic_prompt` | **Chosen.** Context is per-invoke, never saved in the checkpoint; the system prompt is rebuilt on every model call, so it never accumulates and is not affected by message trimming. |
| System message in the `messages` input | Rejected. It becomes a regular message, is persisted in the checkpoint, accumulates each turn and can go stale. |
| `state_schema` | Rejected. Persists entities in the checkpoint, duplicating `session_data` as source of truth. |
| Tool using `ToolRuntime` | Rejected as the main mechanism. The model decides whether to call it, so it is unreliable. Context stays available to tools via `runtime.context` anyway. |
| `store` | Rejected. Only useful for sharing data across threads/sessions. |

**Consequences**

- `self.session_data` is the single source of truth for entities; the checkpointer holds only `messages`.
- One-turn lag: entities are extracted *after* the answer, in the background, so turn N sees data up to turn N-1 (or N-2 if the next message arrives before the extraction ends).
- Errors in the background task are not propagated to the caller; an unhandled exception only surfaces as a "Task exception was never retrieved" warning.
- The task is not strongly referenced, so in theory the event loop could garbage-collect it; accepted for simplicity.
- Async-only hook: the agent must be run with `ainvoke`; `invoke` would fail because no sync hook exists.
- Entities are sent to the LLM in the prompt (privacy consideration, same as the extractor).
- `_trim_messages` only trims `messages`, so entities are never lost when history is trimmed.

### Known design trade-offs (entity extraction)

- **Trimming can be more aggressive.** Key user data lives in `SessionEntity` (not in the message history), so `max_memory_token` can be lowered. Keeping too much text in the context pushes the model to lose focus, and the problem grows with very long chats.
- **Entity memory must stay small.** Everything in `SessionEntity` is injected in every system prompt, so unbounded growth would inflate the context again. Prompting strategies for the extractor (extract only relevant, stable fields; no free text) are to be evaluated to limit what is stored.

### Entity memory management (storage of relevant info)

The entity memory is the deterministic store for the relevant information of a session. It replaces summarization (see D-002): exact values are kept as structured fields instead of being rewritten by an LLM.

- **Schema-driven.** Only fields declared in `SessionEntityData` (and nested models such as `UserInfo`, `AddressInfo`) can be stored. Adding a new kind of relevant info (e.g. an order id) means adding a typed field, not storing free text.
- **Scope.** One `SessionEntity` per `sessionId`, held in `CustomerCareAgent.session_data`. It lives in process memory: it is lost on restart and not shared across instances. Persistence (DB/Redis) is not covered yet.
- **Write path.** Only the background extractor writes, via `merge_data`, after each answer. The main agent never writes entities directly.
- **Merge policy.** Field by field, recursive on nested models. A new non-`None` value overwrites the old one; `None` never erases an existing value.
- **Read path.** Every model call receives the current entities in the system prompt (`entities_prompt`), so they are never affected by trimming.
- **Limits by design.** Bounded size comes from the schema (typed, finite fields) and from the extractor prompt (extract only stable, relevant data). Open points to evaluate:
  - how to correct a wrong value: today the latest extraction wins, so a mistaken extraction overwrites a correct value;
  - how to explicitly delete or invalidate a value when the user retracts it, since `None` is ignored;
  - which entities are relevant for the use case (order ids, issue references, contact data) and their validation (formats, e.g. order id pattern);
  - persistence and expiry of the entity memory per session.

## D-002 — Short-term memory: trimming, not summarization

**Decision.** Keep trimming (`_trim_messages`) as the short-term memory strategy; do not introduce summarization.

**Why summarization does not make sense here**

The agent operates in a context close to AMS (application management support): little text, few but highly relevant pieces of information, aimed at creating and solving very specific issues. This implies that:

1. In most use cases the context is not large, so there is little to gain from compressing it.
2. Summarization introduces non-determinism in how the context is built. A summary may report untrue or slightly different data, e.g. a wrong digit in an order id, and mislead the rest of the conversation.

**Consequences**

- Exact values (ids, names, emails) are preserved verbatim in the message history, or in the entity memory.
- When history exceeds the token limit, the oldest messages are dropped rather than rewritten.
