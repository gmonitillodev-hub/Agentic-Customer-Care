from typing import Optional

from agentic_customer_care.agent.workflow import CustomerCareAgent
from fastapi import FastAPI, HTTPException, Response, Cookie
import os
import uvicorn

from pydantic import BaseModel

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
    
        agent_answer, sessionId = cc_agent.interact(sessionId, payload.message)
  
        """ 
            Set sessionId cookie that will be used in next iterations 
        """  
        response.set_cookie(key="sessionId", value=sessionId)

        return agent_answer
    
    except Exception as e:
        
        print("🚀 ~ chat_inference ~ e:", e)
        raise HTTPException(status_code=500, detail=f"Internal Server Error. Sorry, something went wrong. - Details: {e}")
        
    

    
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
        
        print(f"    Error initialing Agent gateway - Details: {e}")