# Architecture

Rationale behind each choice is logged in [decisions.md](decisions.md).

## Request flow

1. The client calls `POST /inference` (FastAPI, `api_gateway/fast_api.py`); the `sessionId` cookie identifies the conversation.
2. `CustomerCareAgent.interact` (`agent/workflow.py`) resolves or creates the session, trims the history and runs the agent with `ainvoke`.
3. The agent loops (ReAct): it picks a tool, reads the result, and iterates until it can answer.
4. The response is returned and, in the background, the entity extractor updates the session entities.

## Tools

All tools are registered in `src/agentic_customer_care/agent/tools/tools_index.py`.

| Tool | Module | Purpose |
|------|--------|---------|
| `retrieve_documents_from_rag` | `tools/rag.py` | Searches the knowledge base (product sheets, growing guides, policies) with semantic + keyword (BM25) retrieval, grounding answers in verified company information. |
| `get_order_status` | `tools/oms.py` | Returns only the status of an order by ID (format `ORD-XXX`). |
| `get_order_details` | `tools/oms.py` | Returns full order information (status, shipping, estimated delivery) from the orders database. |
| `escalate_request_to_human` | `tools/request_handler.py` | Sends an email to the support team (SMTP) when confidence is low, the request is out of scope, or the customer asks for a human. |
| `get_current_context` | `tools/request_handler.py` | Provides extra context such as user region/city and current datetime (e.g. the current month, without asking the user). |

Tools can read session entities through `runtime.context`.

## Memory

The agent has three memory layers.

| Layer | Mechanism | Scope | Persistence |
|-------|-----------|-------|-------------|
| Short-term | Message history in a LangGraph `InMemorySaver`, trimmed | per `sessionId` | in process |
| Entity memory | `SessionEntity` in `CustomerCareAgent.session_data` | per `sessionId` | in process |
| Long-term | RAG over `knowledge_base/` (Chroma) | global | on disk |

Everything in process is lost on restart and not shared across instances.

### Short-term memory: trimming (D-002)

- The checkpointer holds only `messages`, keyed by `thread_id = sessionId`.
- Before each turn `_trim_messages` applies `trim_messages` (strategy `last`, system message kept, starts on a human message) with `MAX_MEMORY_TOKEN` (`src/utils/constants.py`, default `2000`) and approximate token counting.
- When the limit is exceeded the oldest messages are dropped, never rewritten.
- **Summarization is intentionally not used.** The domain (AMS-like support) has short contexts with few, critical values; an LLM summary is non-deterministic and could alter data (e.g. a wrong digit in an order id). Exact values stay verbatim in the history or in the entity memory.
- Because key user data lives in the entity memory, `MAX_MEMORY_TOKEN` can be lowered: shorter context helps the model stay focused.

### Entity memory (D-001)

Deterministic, schema-driven store (`SessionEntity`, typed fields such as `UserInfo`, `AddressInfo`) for the key data of a session: name, surname, email, address. It lives in `CustomerCareAgent.session_data`, keyed by `sessionId`, and is the single source of truth for entities (the checkpointer holds only `messages`).

- **Write:** after each answer, `EntityExtractorAgent` runs in the background (`@after_agent` middleware, `asyncio.create_task` + `to_thread`) and deep-merges its result via `merge_data`. A new non-`None` value overwrites the old one; `None` never erases. The main agent never writes entities.
- **Read:** a `@dynamic_prompt` middleware rebuilds the system prompt on every model call as base prompt + known entities, passed via `context_schema`. Entities are never stored in the checkpoint, so they don't accumulate and are unaffected by trimming.
- **Trade-offs:** one-turn lag (turn N sees data up to N-1); the agent must run with `ainvoke`; background errors are not propagated; entities are sent to the LLM.
- **Open points:** correcting or retracting a wrong value, entity validation, persistence/expiry, and keeping the extractor limited to stable fields.

### Long-term memory

A RAG layer over `knowledge_base/documents` (topics: `faq`, `garden_info`, `platform_errors`, `policies`) gives the agent product information, policies and agronomic guides across sessions, independently of the current conversation. It is global (not per session) and persisted on disk.

**Ingestion** (`poetry run ingest`, `rag/ingestion.py`):

1. **Extract:** read every file under `knowledge_base/documents/<topic>/` into a `Document` with metadata `topic` and `source`.
2. **Preprocess:** Markdown → HTML → plain text (`markdown2` + BeautifulSoup), whitespace collapsed, headings and tags removed.
3. **Chunk:** `RecursiveCharacterTextSplitter` with `chunk_size=1000`, `chunk_overlap=200`, separators `["\n\n", "\n", " ", ""]`. Overlap preserves context across chunk boundaries. Chunks keep the document metadata and are saved to `knowledge_base/ingestion/chunks.jsonl`.
4. **Embed and index:** chunks are embedded with the provider set by `EMBEDDING_PROVIDER` (`huggingface` or `openai`) and persisted in Chroma at `knowledge_base/vectorstore`. The script asks whether to clear the existing collection first.

**Retrieval** (`rag/retrival.py`, `HybridRetriever`): hybrid search with a LangChain `EnsembleRetriever` that merges two retrievers with weighted Reciprocal Rank Fusion:

| Retriever | Source | Strength | Default weight |
|-----------|--------|----------|----------------|
| Semantic | Chroma vector store | meaning, paraphrases | `semantic_ratio = 0.6` |
| BM25 | `chunks.jsonl` | exact keywords (ids, product names, error codes) | `1 - semantic_ratio = 0.4` |

- Each retriever returns its top `k` chunks; the ensemble fuses the rankings and keeps the first `top_k` (default `5`).
- `semantic_ratio` must be in `[0, 1]`, otherwise a `ValueError` is raised.
- `HybridRetriever` is a thread-safe singleton: embeddings, Chroma and chunks load once and are reused, reducing time to first token. The BM25 index is rebuilt from the chunks on each query.
- The `retrieve_documents_from_rag` tool strips the query, rejects empty ones and calls `retrieve(query, top_k=5)`. Queries must be in English, since the knowledge base is in English.
- Re-run `poetry run ingest` after changing documents: both the vector store and `chunks.jsonl` must be rebuilt so the two retrievers stay aligned.
