
from pathlib import Path
from langchain_core.tools import tool
from utils.functions import get_project_root 
from utils.logger import setup_logger
import json

logger = setup_logger("tools")


def load_orders_from_kb() -> list[dict]:
    """
    Load orders from the knowledge base folder and return them as a list of dictionaries.

    Returns:
        list[dict]: A list of dictionaries containing the content and metadata of each order.
    """
    orders_kb = Path(get_project_root() / "knowledge_base" / "orders") 
    
    if not orders_kb.exists():
        logger.error(f"Orders knowledge base not found: {orders_kb}")
        raise ValueError("Orders knowledge base not found.")
    orders:list = []

    try:
        for order_file in orders_kb.iterdir():
            if order_file.is_file() and order_file.suffix == ".json":
                with open(order_file, "r", encoding="utf-8") as f:
                    order_data = json.load(f)
                    orders.extend(order_data.get("orders", []))
                    
    except Exception as e:
        logger.error(f"Error loading orders from knowledge base: {e}")
        raise ValueError(f"Error loading orders from knowledge base: {e}")

    logger.debug(f"Loaded {len(orders)} orders from knowledge base")
    return orders

@tool
def get_order_status(order_id: str) -> str:
    """
    Get the status of an order from the Order Management System (OMS).

    Args:
        order_id (str): The unique identifier of the order.
    
    Returns:
        str: The status of the order.
        
    Raises:
        ValueError: If the order_id is empty or contains only whitespace or if the order is not found in the knowledge base.
    
    """
        
    logger.info(f"Tool get_order_status called - order_id: {order_id}")
    if not order_id.strip():
        logger.error("get_order_status: empty order_id")
        raise ValueError("Order ID cannot be empty or whitespace.")
    
    orders = load_orders_from_kb()

    requested_order = [order for order in orders if order.get("order_id") == order_id]
    if not requested_order:
        logger.error(f"get_order_status: order not found - order_id: {order_id}")
        raise ValueError("Order not found.")

    return requested_order[0].get("status")

def get_order_details(order_id: str) -> dict:
    """
    Get the details of an order from the Order Management System (OMS).

    Args:
        order_id (str): The unique identifier of the order.

    Returns:
        dict: A dictionary containing the details of the order.

    Raises:
        ValueError: If the order_id is empty or contains only whitespace or if the order is not found in the knowledge base.
    """
    logger.info(f"Tool get_order_details called - order_id: {order_id}")
    if not order_id.strip():
        logger.error("get_order_details: empty order_id")
        raise ValueError("Order ID cannot be empty or whitespace.")

    orders = load_orders_from_kb()

    requested_order = [order for order in orders if order.get("order_id") == order_id]
    if not requested_order:
        logger.error(f"get_order_details: order not found - order_id: {order_id}")
        raise ValueError("Order not found.")

    return requested_order[0]

if __name__ == "__main__":
    order_id = "ORD-001"
    status = get_order_status(order_id)
    print(f"Order ID: {order_id}, Status: {status}")