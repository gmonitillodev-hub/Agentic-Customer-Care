import os
import uuid

from dotenv import load_dotenv

from agentic_customer_care.agent.tools.tools_index import get_all_tools
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver

from utils.constants import CC_AGENT_SYSTEM_PROMPT

load_dotenv()


class CustomerCareAgent:

    def __init__(self, thread_id: str | None = None):
        self.tools = get_all_tools()
        self.thread_id = thread_id or str(uuid.uuid4())
        self.agent = None
        self.init_agent()

    def init_agent(self):
        model = init_chat_model(
            model="openai/gpt-oss-120b",
            model_provider="openai",
            temperature=0,  # deterministic, more reliable for QA
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_API_BASE") or None
        )
        self.agent = create_agent(
            model=model,
            tools=self.tools,
            system_prompt=CC_AGENT_SYSTEM_PROMPT,
            checkpointer=InMemorySaver(),
            debug=os.getenv("AGENT_VERBOSE", "false").lower() == "true",
        )

    def interact(self, message: str) -> str:
        result = self.agent.invoke(
            {"messages": [{"role": "user", "content": message}]},
            config={"configurable": {"thread_id": self.thread_id}},
        )
        return result["messages"][-1].content


if __name__ == "__main__":
    agent = CustomerCareAgent()
    print("Customer care agent (type 'exit' to quit)")
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            break
        if user_input:
            print(f"\nAgent: {agent.interact(user_input)}")
