"""Agent module."""

from pydantic_ai import Agent
from dotenv import load_dotenv
from pydantic import BaseModel
from a2a.types import AgentSkill

from src.mcp_servers import todoist_server
from src.agents.common.agent import load_agent_config

load_dotenv(override=True)

todoist_agent_config = load_agent_config("src/agents/todoist_agent/config.yml")


class TodoistAgentCard(BaseModel):
    """
    Todoist Agent Card.
    """

    name: str = todoist_agent_config.name
    description: str = todoist_agent_config.description
    skills: list[AgentSkill] = []
    organization: str = todoist_agent_config.name
    url: str = todoist_agent_config.endpoint


todoist_agent = Agent(
    model=todoist_agent_config.model,
    mcp_servers=[todoist_server],
    name=todoist_agent_config.name,
    system_prompt=todoist_agent_config.system_prompt,
)


async def run_todoist_agent(task: str) -> str:
    """
    Processes a user task request by running it through the Todoist Agent within the MCP server context.

    Parameters:
        task (str): The user's Todoist-related request in natural language.

    Returns:
        str: The agent's response after processing the task.
    """
    async with todoist_agent.run_mcp_servers():
        result = await todoist_agent.run(
            task,
        )
        return result.output


app = todoist_agent.to_a2a()
