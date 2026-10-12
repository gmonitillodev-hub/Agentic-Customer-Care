from agentic_customer_care.rag.retrival import DocumentFromKB, retrieve_documents_from_vectorstore
from langchain_core.tools import tool 

@tool
def retrieve_documents_from_rag(query: str) -> list[DocumentFromKB]:
    """
    Retrieve documents from the vectorstore based on a query.
    Is needed a preprocess step to ensure the query is in English language before calling this function
    and contains only the relevant information to retrieve documents from the vectorstore. 
    
    Args:
        query (str): The query string to search for. In English language, e.g., "What are the benefits of using AI in customer service?"

    Returns:
        list[DocumentFromKB]: A list of retrieved DocumentFromKB objects.
        
    Raises:
        ValueError: If the query is empty or contains only whitespace.
    """
    
    query = query.strip()
    query = query.replace("\n", " ")
    
    if not query:
        raise ValueError("Query cannot be empty or whitespace.")
    
    return retrieve_documents_from_vectorstore(query, top_k=5)