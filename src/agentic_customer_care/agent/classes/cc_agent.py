from pydantic import BaseModel, Field

class AgentResponse(BaseModel):
    """Send the reply to the user. MUST be called to deliver every message to the user
    (greetings, clarifying questions, refusals and final answers), after any data tool needed."""
    answer: str = Field(description="The reply shown to the user, in the user's language, concise and formal")
    confidence: float = Field(description="A score from 0 to 10")
    sources: str = Field(description="Source of data used: KB, ConversationContext, Other")
    needs_humans: bool = Field(description="True if a human operator is needed")

class InteractResponse(BaseModel):
    data: AgentResponse
    sessionId: str