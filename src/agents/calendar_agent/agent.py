"""Agent module."""

from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic import BaseModel
from a2a.types import AgentSkill

from src.mcp_servers import gcal_server
from src.agents.common.agent import load_agent_config

load_dotenv(override=True)

calendar_agent_config = load_agent_config("src/agents/calendar_agent/config.yml")


class CalendarAgentCard(BaseModel):
    """
    Calendar Agent Card.
    """

    name: str = calendar_agent_config.name
    description: str = calendar_agent_config.description
    skills: list[AgentSkill] = []
    organization: str = calendar_agent_config.name
    url: str = calendar_agent_config.endpoint


calendar_agent = Agent(
    name=calendar_agent_config.name,
    model=calendar_agent_config.model,
    mcp_servers=[gcal_server],
    system_prompt=calendar_agent_config.system_prompt,
)


async def run_calendar_agent(task: str) -> str:
    """
    Runs the calendar agent asynchronously to process a specified task and returns the agent's response.
    
    Parameters:
        task (str): The instruction or request for the calendar agent to handle.
    
    Returns:
        str: The output produced by the calendar agent for the given task.
    """
    async with calendar_agent.run_mcp_servers():
        result = await calendar_agent.run(
            task,
        )
        return result.output


app = calendar_agent.to_a2a()
