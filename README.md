# Agentic Customer Care

**AI-powered customer care agent for GreenThumb Marketplace — faster answers, happier gardeners.**

---

## Project Overview

GreenThumb Marketplace is an e-commerce platform specialized in gardening supplies: seeds, bulbs, tools, pots, soil, and fertilizers. The customer care team handles hundreds of heterogeneous daily requests — product inquiries, order tracking, seasonal agronomic advice, returns and refunds. With a small team and significant volume spikes during spring and autumn, response times become unacceptable.

This project introduces an AI-powered agent that autonomously handles first-level customer requests and intelligently escalates to a human operator when needed. The agent uses a **ReAct reasoning loop** to decide which tool to invoke at each step, ensuring transparent and traceable decision-making throughout every interaction.

## Key Features

- **Conversational AI agent with autonomous reasoning** (ReAct loop)
- **Product catalog search** powered by RAG over a vector store
- **Real-time order status lookup**
- **Intelligent escalation** to human operators
- **Structured JSON output** with answer, confidence score, sources, and escalation flag
- **Short-term conversation memory** (trimming/summarization)
- **Long-term semantic memory** (RAG) over company knowledge base

## Architecture (High-Level)

The system follows a straightforward conversational flow. The user sends a message, and the agent enters a reasoning loop where it analyzes the request and selects the most appropriate tool — catalog search, order lookup, or human escalation. Once the selected tool is executed and its output is collected, the agent formulates a structured response that includes the answer, a confidence score, source references, and an escalation flag if needed. This loop may iterate multiple times for complex queries that require information from more than one source before a final response is delivered to the user.

> 📐 For detailed architecture diagrams and component descriptions, see [Architecture Documentation](docs/architecture.md)

## Tools

### Catalog Search

Searches the company knowledge base — including product sheets, growing guides, and return policies — using semantic retrieval. Returns relevant passages to ground the agent's answer in verified, up-to-date company information.

### Order Status

Looks up order information (status, shipping, estimated delivery) from the orders database. Allows customers to check their order in real time without waiting for a human operator.

### Human Escalation

Transfers the conversation to a human operator when the agent's confidence is low, the request is out of scope, or the customer explicitly asks for human support. Ensures that complex or sensitive issues always receive appropriate attention.

## Memory Strategy

**Short-Term Memory**: The agent maintains conversation context within a session using an explicit strategy (trimming or summarization) to stay within token limits while preserving relevant context. This ensures that multi-turn conversations remain coherent without degrading performance as the dialogue grows longer.

**Long-Term Memory**: A semantic memory layer (RAG) over the company knowledge base allows the agent to retrieve product information, policies, and agronomic guides across sessions. This means the agent always has access to the latest company knowledge, regardless of whether the information appeared in the current conversation.

## Evaluation

The agent is evaluated on a dedicated test dataset using established LLM evaluation frameworks (RAGAS and DeepEval) to measure retrieval quality, answer faithfulness, and overall response accuracy. This ensures that the agent's performance is quantifiable, reproducible, and continuously monitored against defined quality benchmarks.

> 📊 For evaluation methodology, metrics, and results, see [Evaluation Documentation](docs/evaluation.md)

## Getting Started

### Prerequisites

- `<TBD>`

### Installation

```bash
# <TBD>
```

### Environment Setup

Create a `.env` file in the project root:

```env
# <TBD>
```

### Run

```bash
# <TBD>
```

## Project Structure

```
greenthumb-agent/
├── app/
│   ├── agent/
│   ├── tools/
│   ├── memory/
│   └── api/
├── data/
│   ├── knowledge_base/
│   └── orders.json
├── docs/
│   ├── architecture.md
│   └── evaluation.md
├── tests/
├── .env.example
├── requirements.txt
└── README.md
```

## Data & Mock Assets

Since production data cannot be shared, the project includes **fictional but realistic mock data** designed to simulate real-world customer care scenarios:

- **Knowledge Base** — 30+ documents including product sheets, seasonal growing guides, and return/refund policies.
- **Orders** — An `orders.json` file with 20+ mock orders covering various statuses (processing, shipped, delivered, returned).

These assets are sufficient to demonstrate the full capabilities of the agent and to run the evaluation pipeline end to end.

## Documentation

- [Architecture Documentation](docs/architecture.md) — System design, component diagrams, data flow
- [Evaluation Documentation](docs/evaluation.md) — Test dataset, metrics, benchmark results