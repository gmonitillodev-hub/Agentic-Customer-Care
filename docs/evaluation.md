# Evaluation

Evaluation of the RAG (long-term memory) with [RAGAS](https://docs.ragas.io). Retrieval design is described in [architecture.md](architecture.md) and the reasoning in [decisions.md](decisions.md) (D-003).

## Evaluator

Code: `src/agentic_customer_care/rag/evaluation/ragas_evauation.py`. Run with:

```bash
poetry run evaluate_rag
```

It asks for `top_k` and `semantic_ratio` (0–1, 1 = fully semantic) and then:

1. For each test case, retrieves chunks with `HybridRetriever` using the given parameters.
2. Generates an answer with a stuff-documents chain: the LLM must answer **only** from the retrieved documents and say so if the information is missing (temperature 0).
3. Builds a RAGAS dataset (`question`, `answer`, retrieved contexts, `ground_truth`) and scores it.
4. Prints models, retrieval parameters, number of cases and metrics.

Only retrieval + grounded generation is evaluated; the agent loop, tools and memory are not part of this pipeline.

**Models.** The same LLM is used for answer generation and as RAGAS judge (`EXTRACTOR_LLM_PROVIDER` / `EXTRACTOR_LLM_MODEL`). Embeddings come from `EMBEDDING_PROVIDER` / `EMBEDDING_MODEL_NAME`.

### Metrics

| Metric | What it measures |
|--------|------------------|
| `faithfulness` | Whether the answer is supported by the retrieved contexts (low = hallucination). |
| `answer_relevancy` | Whether the answer addresses the question. |
| `context_recall` | Whether the retrieved contexts contain the information of the ground truth (retrieval quality). |

## Test dataset

`eval_dataset_25.py` (`EVAL_DATASET_25`, the one used by the evaluator) contains 25 hand-written cases, each with a `question` and a reference `ground_truth`, spread across the KB topics:

| Topic | Cases |
|-------|-------|
| `faq` | 3 |
| `policies` | 5 |
| `platform_errors` | 3 |
| `garden_info` | 14 |

`eval_dataset.py` holds an extended set of 50 cases with the same topics; it is not used by default.

## Test runs

### Run 1 — fully semantic, large chunks

| Parameter | Value |
|-----------|-------|
| Chunk size | 2000 tokens |
| `top_k` | 5 |
| `semantic_ratio` | 1.0 (semantic only, BM25 disabled) |
| Generation / judge model | `openai/gpt-oss-20b` |
| Test cases | 25 |

| Metric | Score |
|--------|-------|
| Faithfulness | 0.8519 |
| Answer relevancy | 0.8399 |
| Context recall | 1.0000 |

**Reading.** Context recall is perfect: with large chunks the relevant information is always retrieved. Faithfulness and relevancy are lower, probably because large chunks carry a lot of unrelated text that distracts the model.

### Run 2 — hybrid retrieval (50/50)

| Parameter | Value |
|-----------|-------|
| Chunk size | 2000 tokens |
| `top_k` | 5 |
| `semantic_ratio` | 0.5 (50% semantic, 50% BM25) |
| Extractor model | `openai/gpt-oss-20b` |
| Test cases | 25 |

| Metric | Score |
|--------|-------|
| Faithfulness | 0.8805 |
| Answer relevancy | 0.8140 |
| Context recall | 0.9167 |

**Reading.** Compared with Run 1, faithfulness improves (0.8519 → 0.8805): BM25 plus semantic search surfaces more precise chunks, so answers rely better on the retrieved context. Context recall drops (1.0000 → 0.9167) and answer relevancy falls slightly (0.8399 → 0.8140). Without the fully semantic ranking, some relevant chunks are missed, and keyword matches may add less useful context. The run changes several things at once (retrieval mode, and possibly chunking), so the differences cannot be attributed to a single parameter.
