from agentic_customer_care.rag.evaluation.eval_dataset import EVAL_DATASET
from agentic_customer_care.rag.evaluation.eval_dataset_25 import EVAL_DATASET_25
from agentic_customer_care.rag.retrival import HybridRetriever
import os
import sys
import time
import types

from langchain.chat_models import init_chat_model

# ragas 0.4.3 imports a module removed in langchain-community 0.4; stub it (used only for isinstance checks)
if "langchain_community.chat_models.vertexai" not in sys.modules:
    _vertexai_stub = types.ModuleType("langchain_community.chat_models.vertexai")
    _vertexai_stub.ChatVertexAI = type("ChatVertexAI", (), {})
    sys.modules["langchain_community.chat_models.vertexai"] = _vertexai_stub

from ragas import evaluate, EvaluationDataset, SingleTurnSample
from ragas.metrics import LLMContextRecall, Faithfulness, FactualCorrectness, ResponseRelevancy
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from agentic_customer_care.providers.embedding_model_provider.embedding_provider import EmbeddingProviderFactory
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

class RagasEvaluator():
    
    def __init__(self):
        
        self.retriever = HybridRetriever()
        self.model = None
        
        self.extraction_results: list = []
        self.dataset = EVAL_DATASET_25
                 
        self.model = init_chat_model(
            model=os.getenv("EXTRACTOR_LLM_MODEL","openai/gpt-oss-120b"),
            model_provider=os.getenv("EXTRACTOR_LLM_PROVIDER","openai"),
            temperature=0, 
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_API_BASE") or None
        )
        
    def extract_results(self, top_k, semantic_ratio):
        
        
        print(f"\n Evaluating rag with {len(self.dataset)} test cases")
        for test_case in self.dataset:
            
            test_result = self.retrieve_data_from_kb(test_case["question"], top_k, semantic_ratio)    
            self.extraction_results.append(
                {
                    "question": test_case["question"],
                    "answer": test_result["answer"],
                    "context": test_result["chunks"],
                    "ground_truth": test_case["ground_truth"]
                }
            )
            
        print(f"    Data retrieved from KB !!")

    def retrieve_data_from_kb(self, query, top_k, semantic_ratio):
                  
        t0 = time.time()

        docs_retrieved = self.retriever.retrieve(query,  top_k, semantic_ratio)
        latency_retrieval = time.time() - t0

        prompt_template = ChatPromptTemplate.from_template("""
            You are an expert assistant. Answer ONLY based on available documents.
            If the information is not prensent, return a direct response without generate random content
            
            DOCUMENTs:
            {context}

            QUESTION: {input}

            ANSWER:"""
        )
        
        document_chain = create_stuff_documents_chain(self.model, prompt_template)

        t1 = time.time()
        answer = document_chain.invoke({
            "input": query,
            "context": docs_retrieved,
        })
        latency_generation = time.time() - t1

        return {
            "query":              query,
            "chunks":             docs_retrieved,
            "answer":             answer,
            "latency_retrieval":  round(latency_retrieval, 3),
            "latency_generation": round(latency_generation, 3),
            "latency_total":      round(time.time() - t0, 3),
        }
        
    @staticmethod    
    def build_eval_dataset(results: list) -> EvaluationDataset:
        
        print(f"\n  Buiding eval dataset ...")
        samples = [
            SingleTurnSample(
                user_input=r["question"],
                response=r["answer"],
                retrieved_contexts=[doc.page_content for doc in r["context"]],
                reference=r["ground_truth"]
            )
            for r in results
        ]
        return EvaluationDataset(samples=samples)

        
    def ragas_executor(self):
        
        evaluator_llm = LangchainLLMWrapper(self.model)
        # Without explicit embeddings ragas falls back to OpenAI embeddings and the OPENAI_API_KEY
        evaluator_embeddings = LangchainEmbeddingsWrapper(
            EmbeddingProviderFactory.get_embedding_provider().get_embeddings_model()
        )
        
        dataset = self.build_eval_dataset(self.extraction_results)
        print(f"\n  Started RAGAS evaluation ...")
        scores = evaluate(
            dataset=dataset,
            metrics=[
                Faithfulness(),
                ResponseRelevancy(strictness=1),
                LLMContextRecall(),
            ],
            llm=evaluator_llm,
            embeddings=evaluator_embeddings,
        )
        return scores, len(self.dataset)
        
""" Faithfulness = 1.0000
La risposta generata dall’LLM risulta completamente supportata dai context recuperati. Non emergono segnali di hallucination sui casi valutati.

Answer Relevancy = 0.9738
La risposta è fortemente pertinente rispetto alla domanda utente e risponde in modo quasi completo al bisogno informativo.

Context Recall = 1.0000
I context recuperati contengono tutte le informazioni necessarie rispetto alla ground truth/reference. Il retriever sembra quindi recuperare correttamente le informazioni rilevanti. """
    
def evaluate_rag():
    print(f"\n-----------------------------------------------------")
    print("--------------- RAG Evaluator - RAGAS ---------------")
    print(f"-----------------------------------------------------")

    top_k = int(input("\n Insert the top_k value: "))
    print("\n  Semantic ratio is a value that defines the proportion \n between similarity and keyword search (1 full semantic) \n")
    semantic_ratio = float(input("    Insert the semantic ratio (from 0 to 1): "))
    
    evaluator = RagasEvaluator()   
    evaluator.extract_results(top_k, semantic_ratio)
    
    metrics, eval_cases = evaluator.ragas_executor()
    
    print(f"\n    -----------------------------------------------------")
    print(f"    ------------------ Evaluation ended -----------------")
    
    print("\n   Models specifications:")
    print(f"     - Extractor model -> {os.getenv("EXTRACTOR_LLM_MODEL","openai/gpt-oss-20b")}")
    print("\n   Retrival parameters:")
    print(f"     - top_k -> {top_k}")
    print(f"     - semantic_ratio -> {semantic_ratio}")
    print(f"    Number of evaluation cases: {eval_cases}")
    
    print(f"\n    Metrics:")
    print(f"        {metrics}")

    

