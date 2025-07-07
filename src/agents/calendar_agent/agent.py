"""Agent module."""

from datetime import datetime

from dotenv import load_dotenv
from pydantic_ai import Agent
from a2a.types import AgentSkill

from src.mcp_servers import gcal_server
from src.agents.common.agent import load_agent_config
from src.core.logger import logger

load_dotenv(override=True)

# Load configuration
calendar_agent_config = load_agent_config("src/agents/calendar_agent/config.yml")

# Calculate current date for logging
current_date = datetime.now().strftime("%Y-%m-%d")
logger.info("Calendar Agent: Using current date: %s", current_date)

# Format the system prompt and log it
formatted_system_prompt = calendar_agent_config.system_prompt.format(
    current_date=current_date
)
logger.info(
    "Calendar Agent: System prompt after date substitution (first 500 chars): %s...",
    formatted_system_prompt[:500],
)


class CalendarAgentCard:
    """
    Calendar Agent Card.
    """

    name: str = calendar_agent_config.name
    description: str = calendar_agent_config.description
    skills: list[AgentSkill] = []
    organization: str = calendar_agent_config.name
    port: int = calendar_agent_config.port
    host: str = calendar_agent_config.host


# Only add MCP server if it's available
mcp_servers = [gcal_server] if gcal_server else []

calendar_agent = Agent(
    name=calendar_agent_config.name,
    model=calendar_agent_config.model,
    mcp_servers=mcp_servers,
    system_prompt=formatted_system_prompt,
)


async def run_calendar_agent(task: str) -> str:
    """
    Runs the calendar agent asynchronously to process a specified task and returns the agent's response.

    Parameters:
        task (str): The instruction or request for the calendar agent to handle.

    Returns:
        str: The output produced by the calendar agent for the given task.
    """
    # Log the task and current date for debugging
    runtime_date = datetime.now().strftime("%Y-%m-%d")
    logger.info(
        "Calendar Agent: Processing task: '%s' with runtime date: %s",
        task,
        runtime_date,
    )

    if mcp_servers:
        async with calendar_agent.run_mcp_servers():
            result = await calendar_agent.run(
                task,
            )
            return result.output
    else:
        # Run without MCP servers if not available
        result = await calendar_agent.run(
            task,
        )
        return result.output


app = calendar_agent.to_a2a()
