# 🤖 Agentic Customer Care

**AI-powered customer care agent for GreenThumb Marketplace — faster answers, happier gardeners.**

## Overview

GreenThumb Marketplace sells gardening supplies (seeds, bulbs, tools, pots, soil, fertilizers). The customer care team handles many heterogeneous requests — product questions, order tracking, seasonal advice, returns and refunds — with large volume spikes in spring and autumn.

This project is an AI agent that autonomously handles first-level requests and escalates to a human operator when needed. It uses a **ReAct reasoning loop** to choose a tool at each step, keeping every decision traceable.

## Key Features

- Conversational agent with autonomous reasoning (ReAct)
- Knowledge-base search via RAG (semantic + BM25) over a Chroma vector store
- Real-time order status and details lookup
- Escalation to human operators via email
- Short-term (trimming) and long-term (RAG) memory
- FastAPI gateway with cookie-based sessions
- RAGAS-based evaluation

## Architecture

The user sends a message and the agent enters a reasoning loop: it analyzes the request, picks a tool (knowledge-base search, order lookup, human escalation, context), reads the result and iterates if more information is needed before answering.

Tools, memory and session entities are described in [Architecture](docs/architecture.md).

## Getting Started

### Prerequisites

- Python `>=3.13,<4.0`
- [Poetry](https://python-poetry.org/) `>=2`
- An OpenAI-compatible LLM endpoint and API key
- (Optional) An SMTP account, e.g. Mailtrap, for human escalation emails

### Installation

```bash
git clone <repo-url>
cd Agentic-Customer-Care
poetry install
```

### Environment Setup

```bash
cp .env.example .env
```

Then edit `.env`:

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | — | API key for the LLM (and embeddings if `EMBEDDING_PROVIDER=openai`). **Required.** |
| `OPENAI_API_BASE` | official OpenAI | Base URL of an OpenAI-compatible endpoint. |
| `LLM_PROVIDER` | `openai` | Provider of the main agent model. |
| `LLM_MODEL` | `openai/gpt-oss-120b` | Main agent model. |
| `EXTRACTOR_LLM_PROVIDER` | `openai` | Provider of the entity-extractor / evaluation model. |
| `EXTRACTOR_LLM_MODEL` | `openai/gpt-oss-120b` | Entity-extractor / evaluation model. |
| `EMBEDDING_PROVIDER` | `huggingface` | `huggingface` or `openai`. |
| `EMBEDDING_MODEL_NAME` | provider default | Embedding model name. |
| `SMTP_PROVIDER` | `mailtrap` | Email provider for escalations. |
| `SMTP_SERVER` / `SMTP_PORT` | `smtp.mailtrap.io` / `2525` | SMTP host and port. |
| `SMTP_USERNAME` / `SMTP_PASSWORD` | — | SMTP credentials. |
| `SMTP_SENDER` | `no-reply@yourdomain.com` | Sender address. |
| `AGENT_GATEWAY_HOST` / `AGENT_GATEWAY_PORT` | `127.0.0.1` / `8100` | API gateway bind address. |
| `AGENT_VERBOSE` | `false` | Print agent steps to stdout. |

### Commands

Scripts are defined in `pyproject.toml` and run with `poetry run`:

| Command | Description |
|---------|-------------|
| `poetry run ingest` | Chunk and index `knowledge_base/documents` into the vector store. |
| `poetry run run_agent_gateway` | Start the FastAPI gateway (default `http://127.0.0.1:8100`). |
| `poetry run test_retrival` | Smoke-test retrieval from the vector store. |
| `poetry run test_extractor` | Smoke-test the entity extractor. |
| `poetry run evaluate_rag` | Evaluate retrieval with RAGAS. Prompts for `top_k` and `semantic_ratio` (0–1, 1 = fully semantic), then prints the metrics. Uses the `EXTRACTOR_LLM_*` model. |
| `poetry run evaluate_rag_deepeval` | Evaluate retrieval with DeepEval (contextual precision, contextual relevancy, GEval correctness). Same prompts as `evaluate_rag`; many judge calls, mind provider rate limits. |

### Run

```bash
poetry run ingest               # first time only
poetry run run_agent_gateway
```

Try it:

```bash
curl -c cookies.txt -b cookies.txt -X POST http://127.0.0.1:8100/inference \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the status of order ORD-001?"}'
```

The `sessionId` cookie keeps the conversation going across requests.

### API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Health check. |
| `GET` | `/system_info` | Service information. |
| `POST` | `/inference` | Send `{"message": "..."}`; returns the agent response and sets `sessionId` cookie. |
| `GET` | `/session/{session_id}/data` | Export entities collected for a session. |

Interactive docs are available at `/docs`.

## Project Structure

```
.
├── src/
│   ├── agentic_customer_care/
│   │   ├── agent/          # workflow, tools, middlewares, entity extractor, sessions
│   │   ├── api_gateway/    # FastAPI app
│   │   ├── providers/      # embeddings, SMTP
│   │   └── rag/            # ingestion, retrieval, evaluation
│   └── utils/              # constants, logger, helpers
├── knowledge_base/         # documents, orders, products, ingestion chunks, vector store
├── docs/
├── tests/
├── .env.example
└── pyproject.toml
```

## Data & Mock Assets

Production data cannot be shared, so the project ships **fictional but realistic mock data**:

- **Knowledge base** — 30+ documents: growing guides, FAQ, policies, known platform errors.
- **Orders** — `knowledge_base/orders/orders_v1.json`, mock orders across several statuses.
- **Products** — `knowledge_base/products/catalog_v1.json`.

## Evaluation

The agent is evaluated on a dedicated dataset (`src/agentic_customer_care/rag/evaluation/`) with RAGAS to measure retrieval quality and answer faithfulness. Run it with `poetry run evaluate_rag`.

> 📊 Methodology, dataset and results: [Evaluation](docs/evaluation.md)

## Open Points

- **User data management and GDPR compliance.** As a POC, orders and products are read from the knowledge base, and the order tools have direct access to them. In production this would let users retrieve data through the agent, so authentication and authorization must be improved to return only the data each user is entitled to.

## Documentation

- [Architecture](docs/architecture.md) — flow, tools, memory and session entities
- [Evaluation](docs/evaluation.md) — evaluator, test dataset, test runs
- [Design Decisions](docs/decisions.md) — technical decisions and rationale
