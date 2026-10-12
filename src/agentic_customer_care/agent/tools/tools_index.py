from agentic_customer_care.agent.tools.oms import get_order_details, get_order_status
from agentic_customer_care.agent.tools.rag import retrieve_documents_from_rag
from agentic_customer_care.agent.tools.request_handler import escalate_request_to_human, get_current_context

def get_all_tools() -> list[function]:
    """
    Get a list of all available tools.

    Returns:
        list: A list of tool functions.
    """
    
    return [
        retrieve_documents_from_rag,
        get_order_status,
        get_order_details,
        escalate_request_to_human,
        get_current_context    
    ]