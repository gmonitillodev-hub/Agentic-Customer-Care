from agentic_customer_care.agent.workflow import CustomerCareAgent
from fastapi import FastAPI, HTTPException, Response, Cookie
import os
import uvicorn

from pydantic import BaseModel
from utils.logger import setup_logger

logger = setup_logger("agent")

class InferenceRequest(BaseModel):
    message: str


agent_gateway = FastAPI()

cc_agent = CustomerCareAgent()

@agent_gateway.get("/health")
async def health():
    return {"status": "available"}

@agent_gateway.get('/system_info')
async def system_info():
    return {
        "version": "1.0.0",
        "author": "Giuseppe Monitillo",
        "description": "LLM Mock provider - This provider will return always 200 and proper responses",
        "status": "PartiallyAvailable"
    }
    
@agent_gateway.post('/inference')
async def chat_inference(
    payload: InferenceRequest,
    response: Response,
    sessionId = Cookie(None)
):
    
    try:
    
        interect_response = await cc_agent.interact(sessionId, payload.message)
  
        """ 
            Set sessionId cookie that will be used in next iterations 
        """  
        response.set_cookie(key="sessionId", value=interect_response.sessionId)

        return interect_response.data
    
    except Exception as e:
                
        error_message = getattr(e, "message", None) or str(e)
        status_code = getattr(e, "status_code", 500)
        logger.error(f"Inference failed (sessionId: {sessionId}, status: {status_code}): {error_message}")
        raise HTTPException(status_code=status_code, detail=f"Sorry, something went wrong. - Details: {error_message}")
        
    
@agent_gateway.get('/session/{session_id}/data')
def get_session_data(session_id: str):
    
    try:
        return cc_agent.export_session_data(sessionId=session_id)
    
    except Exception as e:
        logger.error(f"Failed to export session data (session_id: {session_id}): {e}")
        return e


    
def init_gateway():    
    
    host = os.getenv("AGENT_GATEWAY_HOST", "127.0.0.1")
    port = int(os.getenv("AGENT_GATEWAY_PORT", "8100"))

    try:
        
        uvicorn.run(
            "agentic_customer_care.api_gateway.fast_api:agent_gateway",
            host=host,
            port=port,
            reload=True,
        )
        
    except Exception as e:
        logger.error(f"Error initializing Agent gateway: {e}")
        print(f"    Error initialing Agent gateway - Details: {e}")