"""Agent module."""

from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic import BaseModel
from a2a.types import AgentSkill
from src.agents.common.agent import load_agent_config

load_dotenv(override=True)


orchestration_agent_config = load_agent_config(
    "src/agents/orchestration_agent/config.yml"
)


class OrchestrationAgentCard(BaseModel):
    """
    Orchestration Agent Card.
    """

    name: str = orchestration_agent_config.name
    description: str = orchestration_agent_config.description
    skills: list[AgentSkill] = []
    organization: str = orchestration_agent_config.name
    url: str = orchestration_agent_config.endpoint


def create_orchestration_agent(tools) -> Agent:
    """
    Creates and returns a personal assistant agent configured with the provided tools and settings from the orchestration agent configuration.
    
    Parameters:
        tools (list): Tool instances to be integrated into the agent.
    
    Returns:
        Agent: A configured agent instance ready to process user requests.
    """
    agent = Agent(
        model=orchestration_agent_config.model,
        name=orchestration_agent_config.name,
        tools=tools,
        system_prompt=orchestration_agent_config.system_prompt,
    )
    return agent
