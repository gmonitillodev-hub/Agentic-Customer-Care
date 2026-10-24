import os

from agentic_customer_care.agent.classes.sessions import SessionEntityData
from dotenv import load_dotenv
import json

from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from pydantic import BaseModel
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage,  AIMessage, ToolMessage


from utils.constants import CC_AGENT_EXTRACTOR_PROMPT
from utils.logger import setup_logger

load_dotenv()

class ExtractorMessage(BaseModel):
    content: str
    source:str
class EntityExtractorAgent:
    
    def __init__(self):
        
        self.agent = None
        
        self.logger = setup_logger("agent", True)
            
        self.init_agent() # Start the initialization


    def init_agent(self):
        """ 
            Agent definition and initialization
        """
        
        model = init_chat_model(
            model=os.getenv("EXTRACTOR_LLM_MODEL","openai/gpt-oss-120b"),
            model_provider=os.getenv("EXTRACTOR_LLM_PROVIDER","openai"),
            temperature=0, 
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_API_BASE") or None
        )
        self.agent = create_agent(
            model=model,
            system_prompt=CC_AGENT_EXTRACTOR_PROMPT,
            response_format=ToolStrategy(SessionEntityData), # Define a tool useful to format the response in a given BaseModel
            debug=os.getenv("AGENT_VERBOSE", "false").lower() == "true",
        )
        


    def invoke(self, context: str) -> SessionEntityData | dict:
        """ 
            Agent invoke with context data.
            
            Args:
                context (str): conversation context
            
            Returns:
                SessionEntityData
        """
        
        messages = self._get_messages_from_context(context)
        if len(messages) == 0:
            return {}
        
        result = self.agent.invoke(self._build_input(messages))
        structured_response = result["structured_response"]
        
        self.logger.info(f"Entity extraction requested")
        self.logger.debug(f"Entity extracted -> {structured_response}")
        
        return structured_response

    @staticmethod
    def _build_input(messages: list[ExtractorMessage]) -> dict:
        serialized_messages = json.dumps([m.model_dump() for m in messages], indent=2, ensure_ascii=False)
        return {"messages": [{"role": "user", "content": serialized_messages}]}
    
    @staticmethod
    def _get_messages_from_context(context) -> list[ExtractorMessage]:
        
        messages = context["messages"]
                
        if not messages or (len(messages) <= 0):
            return []
                
        formatted_messages: list[ExtractorMessage] = []      
        for msg in messages:
                    
            formatted_messages.append( ExtractorMessage(
                content = msg.content or "",
                source  = type(msg).__name__
                ))
            
        return formatted_messages
    

def test_enity_extractor():
   
    EG_CONTEXT = {'messages': [HumanMessage(content='Ciao sono Nicola', additional_kwargs={}, response_metadata={}, id='727f82b3-57b0-4585-8e0c-ec3fb9c36fbb'), AIMessage(content='', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 109, 'prompt_tokens': 872, 'total_tokens': 981, 'completion_tokens_details': {'accepted_prediction_tokens': None, 'audio_tokens': None, 'reasoning_tokens': 89, 'rejected_prediction_tokens': None, 'text_tokens': None}, 'prompt_tokens_details': None, 'queue_time': 0.182525601, 'prompt_time': 0.048779949, 'completion_time': 0.11848283, 'total_time': 0.167262779}, 'model_provider': 'openai', 'model_name': 'openai/gpt-oss-20b', 'system_fingerprint': 'fp_ce54c53bd5', 'id': 'chatcmpl-7d4c7c63-b9cd-4276-8369-0aa496bd6cdf', 'service_tier': 'on_demand', 'finish_reason': 'tool_calls', 'logprobs': None}, id='lc_run--01a148f7-4dcd-7cd3-830b-bedf0d105259-0', tool_calls=[{'name': 'get_current_context', 'args': {}, 'id': 'fc_0ca26183-c162-4527-b686-6b6227eb4c5b', 'type': 'tool_call'}], invalid_tool_calls=[], usage_metadata={'input_tokens': 872, 'output_tokens': 109, 'total_tokens': 981, 'input_token_details': {}, 'output_token_details': {'reasoning': 89}}), ToolMessage(content="location=Location(city='Andria', timezone='Europe/Rome', country='IT', region='Apulia') date_time='2026-10-17 10:25:29'", name='get_current_context', id='9f2516e8-724c-4f17-bb4c-7392514d17b1', tool_call_id='fc_0ca26183-c162-4527-b686-6b6227eb4c5b'), AIMessage(content='', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 86, 'prompt_tokens': 933, 'total_tokens': 1019, 'completion_tokens_details': {'accepted_prediction_tokens': None, 'audio_tokens': None, 'reasoning_tokens': 31, 'rejected_prediction_tokens': None, 'text_tokens': None}, 'prompt_tokens_details': None, 'queue_time': 0.047226204, 'prompt_time': 0.083343906, 'completion_time': 0.088796056, 'total_time': 0.172139962}, 'model_provider': 'openai', 'model_name': 'openai/gpt-oss-20b', 'system_fingerprint': 'fp_d3e146e1a5', 'id': 'chatcmpl-4653213a-6a44-4c9f-8be0-5f4d5d69a662', 'service_tier': 'on_demand', 'finish_reason': 'tool_calls', 'logprobs': None}, id='lc_run--01a148f7-50c2-7061-bdbf-3eafcb80daa8-0', tool_calls=[{'name': 'AgentResponse', 'args': {'answer': 'Ciao Nicola! Come posso aiutarti oggi con i nostri prodotti da giardino?', 'confidence': 9, 'needs_humans': False, 'sources': 'ConversationContext'}, 'id': 'fc_5d92451f-3314-4832-bb83-0a39be0ae887', 'type': 'tool_call'}], invalid_tool_calls=[], usage_metadata={'input_tokens': 933, 'output_tokens': 86, 'total_tokens': 1019, 'input_token_details': {}, 'output_token_details': {'reasoning': 31}}), ToolMessage(content="Returning structured response: answer='Ciao Nicola! Come posso aiutarti oggi con i nostri prodotti da giardino?' confidence=9.0 sources='ConversationContext' needs_humans=False", name='AgentResponse', id='9db025c8-1912-40a2-8093-cdca57cdcc76', tool_call_id='fc_5d92451f-3314-4832-bb83-0a39be0ae887')], 'structured_response': AgentResponse(answer='Ciao Nicola! Come posso aiutarti oggi con i nostri prodotti da giardino?', confidence=9.0, sources='ConversationContext', needs_humans=False)}
   
    agent = EntityExtractorAgent()
    
    result = agent.invoke(EG_CONTEXT)
    res = result["structured_response"].model_dump()
    print("🚀 ~ res:", res)
   