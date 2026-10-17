from pydantic import BaseModel, Field

class AgentResponse(BaseModel):
    answer: str = Field(description="The response of the agent as text")
    confidence: float = Field(description="A score from 0 to 10")
    sources: str = Field(description="Source of data used: KB, ConversationContext, Other")
    needs_humans: bool = Field(description="True if a human operator is needed")

class InteractResponse(BaseModel):
    data: AgentResponse
    sessionId: str