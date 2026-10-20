import os
import uuid

from agentic_customer_care.agent.classes.cc_agent import AgentResponse, InteractResponse
from agentic_customer_care.agent.classes.sessions import SessionEntity
from agentic_customer_care.agent.entity_extractor import EntityExtractorAgent
from agentic_customer_care.agent.middlewares.mw import build_entities_updater, build_prompt_enrichment
from agentic_customer_care.rag.retrival import HybridRetriever
from dotenv import load_dotenv

from agentic_customer_care.agent.tools.tools_index import get_all_tools
from langchain.agents import create_agent

from langchain.agents.structured_output import ToolStrategy
from pydantic import BaseModel, Field
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import RemoveMessage, trim_messages
from langgraph.graph.message import REMOVE_ALL_MESSAGES
from langchain_core.messages.utils import count_tokens_approximately

from utils.constants import CC_AGENT_SYSTEM_PROMPT, MAX_MEMORY_TOKEN
from utils.config import get_config
from utils.functions import _merge_models
from utils.logger import setup_agent_logger

load_dotenv()


class CustomerCareAgent:
    
    def __init__(self):
        
        self.tools = get_all_tools() # Get all fuction / tools typed as StructuredTool that will be passed to the model

        self.logger = setup_agent_logger(True)
        self.agent = None
        
        self.session_data: dict[str, SessionEntity] = {} 
        self.entity_extr_agent = EntityExtractorAgent()
        
        self.kb_retriever = HybridRetriever() # Initialize singleton class of retriever (loads weights just one time at init operation)
        self.init_agent() # Start the initialization

    def init_agent(self):
        
        """ 
            Agent definition and initialization
        """
        model = init_chat_model(
            model=get_config("LLM_MODEL","openai/gpt-oss-20b"),
            model_provider=get_config("LLM_PROVIDER","openai"),
            temperature=0, 
            api_key=get_config("OPENAI_API_KEY"),
            base_url=get_config("OPENAI_API_BASE") or None
        )
        self.agent = create_agent(
            model=model,
            tools=self.tools,
            middleware=[build_prompt_enrichment(CC_AGENT_SYSTEM_PROMPT), build_entities_updater(self.entity_extr_agent)],
            context_schema=SessionEntity,
            response_format=ToolStrategy(AgentResponse), # Define a tool useful to format the response in a given BaseModel
            checkpointer=InMemorySaver(), # Checkpointer based on sessionId
            debug=get_config("AGENT_VERBOSE", "false").lower() == "true",
        )
        
        self.logger.info(f"Customer care Agent initialized - Model: {get_config("LLM_MODEL","openai/gpt-oss-20b")}")
        
        

    async def interact(self, sessionId: str, message: str) -> InteractResponse:
        """ 
            Agent invoke with session data (async).
            
            Args:
                sessionId (UUID)
                message (str): user query
            
            Returns:
                AgentResponse: Structured json response from agent
                sessionId: UUID used to store the historical context
            
            Entity extraction runs in the background after the answer: it is not awaited here.
        """

        sessionId = self._check_session(sessionId=sessionId)
        session_data: SessionEntity = self.session_data[sessionId]
        
        self.logger.info(f"New agent interaction for sessionId: {sessionId}")
        self.logger.debug(f"SessionData of {sessionId} -> {session_data}")
       
        self.checkpointer_config = {"configurable": {"thread_id": sessionId}}
        self._trim_messages()
        
        result = await self.agent.ainvoke(
            {"messages": [{"role": "user", "content": message}]},
            config=self.checkpointer_config,
            context=session_data,
        )
        
        self.logger.debug(f"Response for {sessionId} -> {result}")
        
        return InteractResponse(
                data = result["structured_response"].model_dump(), 
                sessionId = sessionId
            )
        
    def export_session_data(self, sessionId: str) -> SessionEntity:
        """ 
            Return data of a specific session.
        """
        
        if sessionId and sessionId in self.session_data:
            return self.session_data[sessionId]
        
        else:
            raise ValueError("Unknown sessionId")
        
    
    def _check_session(self, sessionId: str | None = None) -> str:
        
        """ 
            Return validated current sessionId or create new one if not exists
                
            Args:
                sessionId (str)
                    
            Returns:
                sessionId (str)
        """
            
        if sessionId and sessionId in self.session_data:
            return sessionId

        sessionId = str(uuid.uuid4())
        self.session_data[sessionId] = SessionEntity(sessionId=sessionId)
        return sessionId

    def _trim_messages(self):
               
        state = self.agent.get_state(self.checkpointer_config)
        history = state.values.get("messages", [])
        if history:
            trimmed = trim_messages(
                history,
                max_tokens=MAX_MEMORY_TOKEN, 
                strategy="last",
                token_counter=count_tokens_approximately,
                include_system=True, start_on="human",
            )
            if len(trimmed) < len(history):
                self.agent.update_state(
                    self.checkpointer_config,
                    {"messages": [RemoveMessage(id=REMOVE_ALL_MESSAGES), *trimmed]},
            )
        
