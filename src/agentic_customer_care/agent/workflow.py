import os
import uuid

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

from utils.constants import CC_AGENT_SYSTEM_PROMPT

load_dotenv()

class AgentResponse(BaseModel):
    answer: str = Field(description="The response of the agent as text")
    confidence: float = Field(description="A score from 0 to 10")
    sources: str = Field(description="Source of data used: KB, ConversationContext, Other")
    needs_humans: bool = Field(description="True if a human operator is needed")

class CustomerCareAgent:
    
    def __init__(self):
        
        self.tools = get_all_tools() # Get all fuction / tools typed as StructuredTool that will be passed to the model
        self.max_memory_token = 2000

        self.agent = None
        
        self.active_sessions: list[str] = []
        
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
            tools=self.tools,
            system_prompt=CC_AGENT_SYSTEM_PROMPT,
            response_format=ToolStrategy(AgentResponse), # Define a tool useful to format the response in a given BaseModel
            checkpointer=InMemorySaver(), # Checkpointer based on sessionId
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
    def interact(self, sessionId: str, message: str):
        
        sessionId = self._check_session(sessionId=sessionId)
        
        self.checkpointer_config = {"configurable": {"thread_id": sessionId}}
        self._trim_messages(sessionId)
        
        result = self.agent.invoke(
            {"messages": [{"role": "user", "content": message}]},
            config=self.checkpointer_config,
        )
        return result["structured_response"].model_dump(), sessionId

    """ 
        Return validated current sessionId or create new one if not exists
        
        Args:
            sessionId (str)
            
        Returns:
            sessionId (str)
    """
    def _check_session(self, sessionId: str | None = None) -> str:
        if not sessionId:
            sessionId = str(uuid.uuid4())
            self.active_sessions.append(sessionId)
            return sessionId

        if sessionId in self.active_sessions:
            return sessionId
        else:
            sessionId = str(uuid.uuid4())
            self.active_sessions.append(sessionId)
            return sessionId
  
    def _trim_messages(self):
               
        state = self.agent.get_state(self.checkpointer_config)
        history = state.values.get("messages", [])
        if history:
            trimmed = trim_messages(
                history,
                max_tokens=self.max_memory_token, 
                strategy="last",
                token_counter=count_tokens_approximately,
                include_system=True, start_on="human",
            )
            if len(trimmed) < len(history):
                self.agent.update_state(
                    self.checkpointer_config,
                    {"messages": [RemoveMessage(id=REMOVE_ALL_MESSAGES), *trimmed]},
            )
        

if __name__ == "__main__":
    agent = CustomerCareAgent()
    
    session = agent.check_session()
    print("🚀 ~ session:", session)
    
    session = agent.check_session(session)
    print("🚀 ~ session:", session)
    
    """ print("Customer care agent (type 'exit' to quit)")
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            break
        if user_input:
            print(f"\nAgent: {agent.interact(user_input)}")
 """