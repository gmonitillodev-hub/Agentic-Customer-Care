import json
import os
import re

os.environ.setdefault("DEEPEVAL_TELEMETRY_OPT_OUT", "YES")  # no data sent to third parties (set before importing deepeval)

from agentic_customer_care.rag.evaluation.ragas_evauation import RagasEvaluator
from deepeval import evaluate
from deepeval.evaluate.configs import AsyncConfig, DisplayConfig
from deepeval.metrics import ContextualPrecisionMetric, ContextualRelevancyMetric, GEval
from deepeval.models import DeepEvalBaseLLM
from deepeval.test_case import LLMTestCase, SingleTurnParams
from langchain.chat_models import init_chat_model


class DeepEvalJudge(DeepEvalBaseLLM):
    """Judge model for DeepEval backed by the same OpenAI-compatible endpoint used by the rest of the project."""

    def __init__(self):
        self.model = init_chat_model(
            model=os.getenv("EXTRACTOR_LLM_MODEL", "openai/gpt-oss-120b"),
            model_provider=os.getenv("EXTRACTOR_LLM_PROVIDER", "openai"),
            temperature=0,
            max_retries=8,  # the provider TPM limit is low: the client backs off on 429
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_API_BASE") or None,
        )

    def load_model(self):
        return self.model

    @staticmethod
    def _parse(text: str, schema):
        """DeepEval metrics ask for a Pydantic schema: extract the JSON object from the model output."""
        match = re.search(r"\{.*\}", text, flags=re.DOTALL)
        return schema(**json.loads(match.group(0) if match else text))

    def generate(self, prompt: str, schema=None):
        text = self.model.invoke(prompt).content
        return self._parse(text, schema) if schema else text

    async def a_generate(self, prompt: str, schema=None):
        text = (await self.model.ainvoke(prompt)).content
        return self._parse(text, schema) if schema else text

    def get_model_name(self):
        return os.getenv("EXTRACTOR_LLM_MODEL", "openai/gpt-oss-120b")


class DeepEvalEvaluator(RagasEvaluator):
    """Reuses retrieval + answer generation of RagasEvaluator and scores the results with DeepEval metrics."""

    def build_test_cases(self) -> list[LLMTestCase]:
        return [
            LLMTestCase(
                input=r["question"],
                actual_output=r["answer"],
                expected_output=r["ground_truth"],
                retrieval_context=[doc.page_content for doc in r["context"]],
            )
            for r in self.extraction_results
        ]

    def deepeval_executor(self, threshold: float = 0.5):

        judge = DeepEvalJudge()
        metrics = [
            ContextualPrecisionMetric(threshold=threshold, model=judge, include_reason=False),
            ContextualRelevancyMetric(threshold=threshold, model=judge, include_reason=False),
            GEval(
                name="Correctness",
                criteria="Determine whether the actual output is factually consistent with the expected output, "
                         "without contradictions and without relevant missing information.",
                evaluation_params=[
                    SingleTurnParams.INPUT,
                    SingleTurnParams.ACTUAL_OUTPUT,
                    SingleTurnParams.EXPECTED_OUTPUT,
                ],
                threshold=threshold,
                model=judge,
            ),
        ]

        print("\n  Started DeepEval evaluation ...")
        result = evaluate(
            test_cases=self.build_test_cases(),
            metrics=metrics,
            async_config=AsyncConfig(run_async=True, max_concurrent=1),  # low concurrency: provider rate limits
            display_config=DisplayConfig(show_indicator=False, print_results=False),
        )
        return self.summarize(result), len(self.dataset)

    @staticmethod
    def summarize(result) -> dict[str, dict]:
        """Average score and pass rate per metric."""
        scores: dict[str, list] = {}
        for test_result in result.test_results:
            for metric in test_result.metrics_data or []:
                scores.setdefault(metric.name, []).append((metric.score, metric.success))
        return {
            name: {
                "mean_score": round(sum(s for s, _ in values if s is not None) / max(len(values), 1), 4),
                "pass_rate": round(sum(1 for _, ok in values if ok) / max(len(values), 1), 4),
            }
            for name, values in scores.items()
        }


def evaluate_rag_deepeval():
    print(f"\n-----------------------------------------------------")
    print("-------------- RAG Evaluator - DeepEval --------------")
    print(f"-----------------------------------------------------")

    top_k = int(input("\n Insert the top_k value: "))
    print("\n  Semantic ratio is a value that defines the proportion \n between similarity and keyword search (1 full semantic) \n")
    semantic_ratio = float(input("    Insert the semantic ratio (from 0 to 1): "))

    evaluator = DeepEvalEvaluator()
    evaluator.extract_results(top_k, semantic_ratio)

    metrics, eval_cases = evaluator.deepeval_executor()

    print(f"\n    -----------------------------------------------------")
    print(f"    ------------------ Evaluation ended -----------------")

    print("\n   Models specifications:")
    print(f"     - Generation / judge model -> {os.getenv('EXTRACTOR_LLM_MODEL', 'openai/gpt-oss-120b')}")
    print("\n   Retrival parameters:")
    print(f"     - top_k -> {top_k}")
    print(f"     - semantic_ratio -> {semantic_ratio}")
    print(f"    Number of evaluation cases: {eval_cases}")

    print(f"\n    Metrics (mean score / pass rate with threshold 0.5):")
    for name, values in metrics.items():
        print(f"        {name}: {values['mean_score']} / {values['pass_rate']}")
