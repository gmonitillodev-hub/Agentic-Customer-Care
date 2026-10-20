

import html
from datetime import datetime
from pydantic import BaseModel
from langchain_core.tools import tool 
import requests
from agentic_customer_care.providers.smtp.smtp_factory import SmtpFactory
from utils.constants import ESCALATION_EMAIL_TEMPLATE
from utils.logger import setup_logger

logger = setup_logger("tools")

@tool
def escalate_request_to_human(message: str) -> str:
    """
    Escalates a request to a human agent.
    In case the AI agent cannot handle a request or if the user explicitly requests human assistance, 
    this function can be called to escalate the request to a human agent for further handling.
    
    An email will be sent to the support team with the details of the request that needs human assistance.

    Args:
        message (str): The message or request that needs to be escalated.
        
    Returns:
        is_success (bool): True if the escalation was successful, False otherwise.
        error (str): Error message if the escalation failed, None otherwise.
    """
    
    logger.info("Tool escalate_request_to_human called")
    logger.debug(f"Escalation message: {message}")
    
    try:
    
        smtp_server = SmtpFactory.init_smtp_provider()
        smtp_server.send_email(
            to_email="g.monitillo.dev@gmail.com",
            subject="Escalated Request to Human Agent",
            body=f"Here is the details:\n\n{message}",
            html_body=ESCALATION_EMAIL_TEMPLATE.format(message=html.escape(message)),
        )
        
    except Exception as e:
        logger.error(f"Failed to escalate request: {e}")
        return {"is_success": False, "error": str(e)}

    logger.info("Request escalated to human agent")
    return {"is_success": True}

class Location(BaseModel):
    city: str
    timezone: str
    country:str
    region:str

class CurrentContext(BaseModel):
    location: Location
    date_time: str

@tool
def get_current_context() -> CurrentContext:
    """
    Retrieves the current context of the conversation or interaction.
    It returns a information object, which can be used to provide 
    additional information to the prompt like location and timestamp.

    Returns:
        location (Location): The location of the current context
        date_time (Date): The date and time of the current context
    """
    
    logger.info("Tool get_current_context called")
    current_date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        resp = requests.get("https://ipinfo.io/json")
        data = resp.json()
        location = Location(
            city=data.get("city"),
            timezone=data.get("timezone"),
            country=data.get("country"),
            region=data.get("region")
        )
    
    except Exception as e:
        logger.error(f"Failed to retrieve current context: {e}")
        location = "Unknown"

    return CurrentContext(
        location=location,
        date_time=current_date_time
        )

if __name__ == "__main__":
    
    print(get_current_context())