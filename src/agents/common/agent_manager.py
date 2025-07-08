"""Agent Manager for handling agent registration and server creation."""

from typing import Dict, List, Type
from dataclasses import dataclass
from a2a.server.apps import A2AStarletteApplication
from pydantic import BaseModel
from pydantic_ai import Agent

from .server import create_agent_a2a_server


@dataclass
class AgentRegistration:
    """Registration information for an agent."""

    card_class: Type[BaseModel]
    agent_instance: Agent
    status_message: str
    artifact_name: str = "response"

    def create_server(self) -> A2AStarletteApplication:
        """Create A2A server for this agent."""
        card = self.card_class()
        return create_agent_a2a_server(
            agent=self.agent_instance,
            name=card.name,
            description=card.description,
            skills=card.skills,
            host=card.host,
            port=card.port,
            status_message=self.status_message,
            artifact_name=self.artifact_name,
        )


class AgentManager:
    """Manager for agent registration and server creation."""

    def __init__(self):
        self._registry: Dict[str, AgentRegistration] = {}

    def register_agent(
        self,
        name: str,
        card_class: Type[BaseModel],
        agent_instance: Agent,
        status_message: str,
        artifact_name: str = "response",
    ) -> None:
        """Register an agent with the manager."""
        self._registry[name] = AgentRegistration(
            card_class=card_class,
            agent_instance=agent_instance,
            status_message=status_message,
            artifact_name=artifact_name,
        )

    def get_agent_list(self) -> List[Dict]:
        """Get list of agents suitable for server startup."""
        agents = []
        for agent_key, registration in self._registry.items():
            card = registration.card_class()
            agents.append(
                {
                    "name": card.name,
                    "agent": registration.create_server,
                    "port": card.port,
                }
            )
        return agents

    def get_agent_registration(self, name: str) -> AgentRegistration:
        """Get agent registration by name."""
        if name not in self._registry:
            raise KeyError(f"Agent '{name}' not found in registry")
        return self._registry[name]

    def list_registered_agents(self) -> List[str]:
        """Get list of registered agent names."""
        return list(self._registry.keys())


# Global agent manager instance
agent_manager = AgentManager()
