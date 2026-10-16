import os
import uuid

from dotenv import load_dotenv

from agentic_customer_care.agent.tools.tools_index import get_all_tools
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from pydantic import BaseModel, Field
from langchain.chat_models import init_chat_model

from utils.constants import CC_AGENT_EXTRACTOR_PROMPT

load_dotenv()

class AddressInfo(BaseModel):
    city: str | None = None
    postal_code: str | None = None
    region: str | None = None

class UserInfo(BaseModel):
    
    name: str | None = None
    surname: str | None = None
    email: str | None = None
    address_info: AddressInfo | None = None

class AgentResponse(BaseModel):
    user_info: UserInfo | None = None
    

class EntityExtractorAgent:
    
    def __init__(self):
        
        self.agent = None
            
        self.init_agent() # Start the initialization

    """ 
        Agent definition and initialization
    """
    def init_agent(self):
        model = init_chat_model(
            model=os.getenv("LLM_MODEL","openai/gpt-oss-20b"),
            model_provider=os.getenv("LLM_PROVIDER","openai"),
            temperature=0, 
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_API_BASE") or None
        )
        self.agent = create_agent(
            model=model,
            system_prompt=CC_AGENT_EXTRACTOR_PROMPT,
            response_format=ToolStrategy(AgentResponse), # Define a tool useful to format the response in a given BaseModel
            debug=os.getenv("AGENT_VERBOSE", "false").lower() == "true",
        )

    """ 
        Agent invoke with session data.
        
        Args:
            sessionId (UUID)
            message (str): user query
        
        Returns:
            AgentResponse: Structured json response from agent
            sessionId: UUID used to store the historical context
    """
    def invoke(self, context: str):
                
        result = self.agent.invoke(
            {"messages": [{"role": "user", "content": context}]}
        )
        return result
  

def test_enity_extractor():
   
    EG_CONTEXT = """ 
    
    [HumanMessage(content='Ciao sono Nicola', additional_kwargs={}, response_metadata={}, id='4b4edf6d-1af5-4e85-afcc-28800c42acd0'), AIMessage(content='', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 109, 'prompt_tokens': 872, 'total_tokens': 981, 'completion_tokens_details': {'accepted_prediction_tokens': None, 'audio_tokens': None, 'reasoning_tokens': 89, 'rejected_prediction_tokens': None, 'text_tokens': None}, 'prompt_tokens_details': None, 'queue_time': 0.03646452, 'prompt_time': 0.043854298, 'completion_time': 0.148842031, 'total_time': 0.192696329}, 'model_provider': 'openai', 'model_name': 'openai/gpt-oss-20b', 'system_fingerprint': 'fp_d3e146e1a5', 'id': 'chatcmpl-11df2e3b-3ccc-4bf7-9581-05e1690a4249', 'service_tier': 'on_demand', 'finish_reason': 'tool_calls', 'logprobs': None}, id='lc_run--01a145d9-e104-7361-81e6-0868ec35eb21-0', tool_calls=[{'name': 'get_current_context', 'args': {}, 'id': 'fc_fcdef7d3-cacf-4dea-9e67-cf04facacaee', 'type': 'tool_call'}], invalid_tool_calls=[], usage_metadata={'input_tokens': 872, 'output_tokens': 109,'total_tokens': 981, 'input_token_details': {}, 'output_token_details': {'reasoning': 89}}), ToolMessage(content="location=Location(city='Andria', timezone='Europe/Rome', country='IT', region='Apulia') date_time='2026-10-16 19:54:29'", name='get_current_context', id='591c7107-c826-484e-a461-8fe0a5338e88', tool_call_id='fc_fcdef7d3-cacf-4dea-9e67-cf04facacaee'), AIMessage(content='', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 118, 'prompt_tokens': 933, 'total_tokens': 1051, 'completion_tokens_details': {'accepted_prediction_tokens': None, 'audio_tokens': None, 'reasoning_tokens': 62, 'rejected_prediction_tokens': None, 'text_tokens': None}, 'prompt_tokens_details': None, 'queue_time': 0.299290368, 'prompt_time': 0.080625336, 'completion_time': 0.129607262, 'total_time': 0.210232598}, 'model_provider': 'openai', 'model_name': 'openai/gpt-oss-20b', 'system_fingerprint': 'fp_a8c584dda7', 'id': 'chatcmpl-7329af78-cdc0-4dd1-876d-85fc0076caa6', 'service_tier': 'on_demand', 'finish_reason': 'tool_calls', 'logprobs': None}, id='lc_run--01a145d9-e3b6-7c21-bcb3-6a492dfd7c24-0', tool_calls=[{'name': 'AgentResponse', 'args': {'answer': 'Ciao Nicola! Come posso aiutarti oggi con i nostri prodotti per il giardino?', 'confidence': 9, 'needs_humans': False, 'sources': 'ConversationContext'}, 'id': 'fc_ba065bdb-5cf8-47fc-87cf-b92c4376ad42', 'type': 'tool_call'}], invalid_tool_calls=[], usage_metadata={'input_tokens': 933, 'output_tokens': 118, 'total_tokens': 1051, 'input_token_details': {}, 'output_token_details': {'reasoning': 62}}), ToolMessage(content="Returning structured response: answer='Ciao Nicola! Come posso aiutarti oggi con i nostri prodotti per il giardino?' confidence=9.0 sources='ConversationContext' needs_humans=False", name='AgentResponse', id='86a4c44f-aa0f-4ad2-8694-87033a747c0b', tool_call_id='fc_ba065bdb-5cf8-47fc-87cf-b92c4376ad42')]
    
    """
   
    agent = EntityExtractorAgent()
    
    result = agent.invoke(EG_CONTEXT)
    res = result["structured_response"].model_dump()
    print("🚀 ~ res:", res)
   