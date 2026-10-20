from agentic_customer_care.rag.retrival import HybridRetriever
from langchain_core.documents import Document
from langchain_core.tools import tool 
from utils.logger import setup_logger

logger = setup_logger("tools")

@tool
def retrieve_documents_from_rag(query: str) -> list[Document]:
    """
    Retrieve documents from the vectorstore based on a query.
    Is needed a preprocess step to ensure the query is in English language before calling this function
    and contains only the relevant information to retrieve documents from the vectorstore. 
    
    Args:
        query (str): The query string to search for. In English language, e.g., "What are the benefits of using AI in customer service?"

    Returns:
        list[Document]: A list of retrieved LangChain Document objects.
        
    Raises:
        ValueError: If the query is empty or contains only whitespace.
    """
    
    query = query.strip()
    query = query.replace("\n", " ")
    
    if not query:
        logger.error("retrieve_documents_from_rag: empty query")
        raise ValueError("Query cannot be empty or whitespace.")
    
    logger.info(f"Tool retrieve_documents_from_rag called - query: {query}")
    docs = HybridRetriever().retrieve(query, top_k=5)
    logger.debug(f"Retrieved {len(docs)} documents: {[d.metadata.get('source') for d in docs]}")
    return docs