from agentic_customer_care.providers.embedding_model_provider.embedding_provider import EmbeddingProviderFactory
from langchain_chroma import Chroma
from utils import get_project_root
from pydantic import BaseModel

class DocumentFromKB(BaseModel):
    page_content: str
    metadata: dict
    score: float
    
def map_retrived_docuents(retrieved_docs: list) -> list[DocumentFromKB]:
    """
    Map the retrieved documents to a list of Document objects.

    Args:
        retrieved_docs (list[tuple[Document, float]]): A list of tuples containing Document objects and their similarity scores.

    Returns:
    """
    
    documents: list = []
    
    for doc, score in retrieved_docs:        
        document = DocumentFromKB(
            page_content=doc.page_content,
            metadata=doc.metadata,
            score=score
        )
        documents.append(document)

    return documents

def retrieve_documents_from_vectorstore(query: str, top_k: int = 5) -> list[DocumentFromKB]:
    """
    Retrieve documents from the vectorstore based on a query.

    Args:
        query (str): The query string to search for.
        top_k (int): The number of top documents to retrieve.

    Returns:
        list[Document]: A list of retrieved Document objects.
    """
    
    embedding_provider = EmbeddingProviderFactory.get_embedding_provider()
    
    # Load the vectorstore
    vectorstore = Chroma(persist_directory=str(get_project_root() / "knowledge_base" / "vectorstore"), 
                         embedding_function=embedding_provider.get_embeddings_model())
    
    # Perform similarity search
    retrieved_docs = vectorstore.similarity_search_with_score(query, k=top_k)
    
    mapped_docs = map_retrived_docuents(retrieved_docs)
    
    return mapped_docs

def test_retrieve_documents_from_vectorstore():
    
    TOP_K = 3
    
    proceed = True
    while proceed:
        
    
        query = input(" Enter a query to retrieve documents from the vectorstore: ")
        retrieved_docs = retrieve_documents_from_vectorstore(query, TOP_K)
        
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