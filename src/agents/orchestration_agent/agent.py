"""Agent module."""

from dotenv import load_dotenv
from pydantic_ai import Agent
from a2a.types import AgentSkill
from src.agents.common.agent import load_agent_config
from src.agents.common.tool_client import A2AToolClient

load_dotenv(override=True)

# Use longer timeout for complex operations like Gmail processing
a2a_client = A2AToolClient(default_timeout=300.0)  # 5 minutes


orchestration_agent_config = load_agent_config(
    "src/agents/orchestration_agent/config.yml"
)


class OrchestrationAgentCard:
    """
    Orchestration Agent Card.
    """

    name: str = orchestration_agent_config.name
    description: str = orchestration_agent_config.description
    skills: list[AgentSkill] = []
    organization: str = orchestration_agent_config.name
    port: int = orchestration_agent_config.port
    host: str = orchestration_agent_config.host


orchestration_agent = Agent(
    model=orchestration_agent_config.model,
    name=orchestration_agent_config.name,
    tools=[a2a_client.list_remote_agents, a2a_client.create_task],
    system_prompt=orchestration_agent_config.system_prompt,
)
