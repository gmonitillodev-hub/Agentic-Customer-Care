from agentic_customer_care.rag.embedding_model_provider.embedding_provider import EmbeddingProviderFactory
from langchain_chroma import Chroma
from utils import get_project_root
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings


def retrieve_documents_from_vectorstore(query: str, top_k: int = 5) -> list[Document]:
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
    retrieved_docs = vectorstore.similarity_search(query, k=top_k)
    
    return retrieved_docs

def test_retrieve_documents_from_vectorstore():
    
    TOP_K = 3
    
    proceed = True
    while proceed:
        
    
        query = input(" Enter a query to retrieve documents from the vectorstore: ")
        retrieved_docs = retrieve_documents_from_vectorstore(query, TOP_K)
        
        print(f"\n    Retrieved {len(retrieved_docs)} documents for query: '{query}'")
        for i, doc in enumerate(retrieved_docs):
            print(f"        Document {i+1}: {doc.page_content}... \n\n")  # Print first 200 characters of each document
            
        user_input = input("    Do you want to test the document retrieval from the vectorstore? (y/n): \n")
        if user_input.lower() == "y":
            proceed = True
            break
        elif user_input.lower() == "n":
            proceed = False
            print(" Skipping document retrieval test.")
            break
        else:
            print(" Invalid input. Please enter 'y' or 'n'.")