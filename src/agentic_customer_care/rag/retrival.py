from pathlib import Path

from agentic_customer_care.providers.embedding_model_provider.embedding_provider import EmbeddingProviderFactory
from langchain_chroma import Chroma
from utils import get_project_root
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever
import json
import threading
from langchain_core.documents import Document


class HybridRetriever:
    """
        Singleton: embeddings, Chroma and chunks are loaded once and reused.
        This avoid wrights loading for each retrieve improving the TTFT.
        
        Singleton because will be used in a tool, so We are confident that will
        not created more instances.
    """

    _instance: "HybridRetriever | None" = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                instance = super().__new__(cls)
                instance._initialized = False
                cls._instance = instance
        return cls._instance

    def __init__(self):
        with self._lock:
            if self._initialized:
                return
            embedding_provider = EmbeddingProviderFactory.get_embedding_provider()
            self._vectorstore = Chroma(
                persist_directory=str(get_project_root() / "knowledge_base" / "vectorstore"),
                embedding_function=embedding_provider.get_embeddings_model(),
            )
            chunks_path = Path(get_project_root() / "knowledge_base" / "ingestion" / "chunks.jsonl")
            self._chunks = []
            with open(chunks_path, "r", encoding="utf-8") as f:
                for line in f:
                    d = json.loads(line)
                    self._chunks.append(Document(page_content=d["page_content"], metadata=d["metadata"]))
            self._initialized = True
            
            

    def retrieve(self, query: str, top_k: int = 5, semantic_ratio: float = 0.6) -> list[Document]:
        
        if not (0.0 <= semantic_ratio <= 1.0):
            raise ValueError("Il parametro semantic_ratio deve essere compreso tra 0 e 1")
    
    # Calcolo automatico del peso per il BM25
        bm25_weight = 1.0 - semantic_ratio
        bm25 = BM25Retriever.from_documents(self._chunks, k=top_k)
        semantic = self._vectorstore.as_retriever(search_kwargs={"k": top_k})
        # Hybrid — 40% BM25, 60% vector
        hybrid = EnsembleRetriever(retrievers=[bm25, semantic], weights=[bm25_weight, semantic_ratio])
        
        return hybrid.invoke(query)[:top_k]



def test_retrieve_documents_from_vectorstore():
    
    TOP_K = 5
    
    proceed = True
    while proceed:
        
    
        query = input(" Enter a query to retrieve documents from the vectorstore: ")
        retrieved_docs = HybridRetriever().retrieve(query, TOP_K)
        
        print(f"\n    Retrieved {len(retrieved_docs)} documents for query: '{query}'")
        for i, doc in enumerate(retrieved_docs):
            print(f"        Document {i+1}: {doc}... \n\n")  # Print first 200 characters of each document
            
        user_input = input("    Do you want to test the document retrieval from the vectorstore? (y/n): \n")
        if user_input.lower() == "y":
            proceed = True
            
        elif user_input.lower() == "n":
            proceed = False
            print(" Skipping document retrieval test.")
            break
        else:
            print(" Invalid input. Please enter 'y' or 'n'.")