from agentic_customer_care.agent.classes.sessions import SessionEntity
from agentic_customer_care.agent.entity_extractor import EntityExtractorAgent
from langchain.agents.middleware import AgentMiddleware, AgentState, ModelRequest, after_agent, dynamic_prompt
import asyncio
from langgraph.runtime import Runtime
from utils.logger import setup_logger

logger = setup_logger("agent")


def build_prompt_enrichment(system_prompt: str):

    @dynamic_prompt
    def entities_prompt(request: ModelRequest[SessionEntity]) -> str:
        """Build the full system prompt, appending known user entities from the runtime context."""
        ctx = request.runtime.context
        known = ctx.data.model_dump(exclude_none=True) if ctx else {}
        if not known:
            return system_prompt
        return f"{system_prompt}\n\nKnown user data (do not ask for it again): {known}"
    return entities_prompt

def build_entities_updater(extractor: EntityExtractorAgent) -> AgentMiddleware:
    """After the agent run, extract entities in the background without delaying the answer.
    
    The hook schedules the extraction with asyncio.create_task (not awaited) and returns
    immediately, so ainvoke() completes and the answer is returned right away.
    Async-only: the agent must be run with ainvoke().
    """
    
    @after_agent
    async def update_entities(state: AgentState, runtime: Runtime[SessionEntity]) -> None:
        async def _extract() -> None:
            # extractor.invoke is sync and blocking: to_thread runs it in a worker thread so the
            # event loop stays free; the await only suspends this task, not the loop.
            # the task is not awaited, so exceptions would otherwise be silently lost
            try:
                extracted = await asyncio.to_thread(extractor.invoke, state)
                if extracted:
                    runtime.context.merge_data(extracted)
                    logger.debug(f"Session entities updated -> {extracted}")
            except Exception as e:
                logger.error(f"Background entity extraction failed: {e}")
    
        asyncio.create_task(_extract())
    return update_entities