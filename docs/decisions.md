# Design Decisions

Log of technical decisions and why they were taken. Newest entries at the bottom. Implementation details are in [architecture.md](architecture.md).

## D-001 — Session entities: dedicated memory injected via dynamic prompt

**Need.** The main agent must know user data (name, surname, email, address) on every turn without re-asking.

**Decision.** Keep entities in a typed `SessionEntity` per session, filled by a background extractor and injected into the system prompt through `context_schema` + `@dynamic_prompt`.

**Why.** It fits this use case: relevant information is saved once and reused to solve problems without asking the user again, even after old messages are trimmed.

**Technical choices**

- Extracting in the background after the answer keeps latency unaffected.
- A schema-driven store is deterministic and bounded in size; exact values are never rewritten by an LLM.
- Per-invoke context is not saved in the checkpoint: the prompt is rebuilt each call, so it never accumulates, never goes stale and is not affected by trimming.
- A single source of truth (`session_data`) avoids duplicating entities in the checkpoint.

**Alternatives rejected**

| Option | Why not |
|---|---|
| System message in `messages` | Persisted in the checkpoint, accumulates each turn, can go stale. |
| `state_schema` | Duplicates `session_data` as source of truth. |
| Tool with `ToolRuntime` | The model decides whether to call it, so it is unreliable. |
| `store` | Only useful to share data across threads/sessions. |

**Accepted trade-offs.** One-turn lag in entity availability; async-only; background errors not propagated; entities are sent to the LLM. Open points (corrections, validation, persistence) are listed in the architecture doc.

## D-002 — Short-term memory: trimming, not summarization

**Decision.** Keep trimming as the short-term memory strategy; do not introduce summarization.

**Why.** The agent works in an AMS-like context: little text, few but critical values (ids, names, emails).

1. Contexts are usually small, so compression gains little.
2. Summarization is non-deterministic and may alter data (e.g. a wrong digit in an order id) and mislead the conversation.

Dropping the oldest messages keeps exact values verbatim, and key user data is preserved anyway by the entity memory.

## D-003 — Long-term memory: deterministic RAG over a topic-organized KB

**Decision.** Long-term memory is a RAG over the knowledge base, organized by topic, using recursive chunking and a hybrid (semantic + BM25) retriever, with no LLM involved in retrieval.

**Why.** The agent must ground answers in verified company information, and the retrieved data must be predictable and reproducible.

**Knowledge base by topic.** Documents are kept in one folder per topic, stored as `topic` metadata on every chunk:

- `faq`
- `garden_info`
- `platform_errors`
- `policies`

**Chunking strategy.** `RecursiveCharacterTextSplitter`, chunks of 1000 characters with 200 overlap, splitting on paragraphs, then lines, then words. Documents are short and self-contained, so this keeps paragraphs together where possible, and the overlap avoids losing context at chunk boundaries. Markdown is converted to plain text first, so formatting noise doesn't enter the embeddings.

**No reranking or LLM augmentation.** Query rewriting, LLM reranking and similar techniques are intentionally not used: they would introduce non-deterministic behavior in KB retrieval, as in D-002. The same query always returns the same chunks, which makes retrieval easy to test and evaluate.

**Hybrid retrieval (semantic + BM25).** The KB contains platform errors (codes, exact messages), where semantic search alone can miss exact matches. An ensemble retriever combines BM25 (keyword) with vector search (meaning), weighted 40/60 by default, so both kinds of query work. Both approaches are deterministic.
