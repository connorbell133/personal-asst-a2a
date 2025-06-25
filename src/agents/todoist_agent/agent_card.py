"""Agent Card module."""

from pydantic import BaseModel
from a2a.types import AgentSkill


class TodoistAgentCard(BaseModel):
    """
    Todoist Agent Card.
    """

    name: str = "Todoist Agent"
    description: str = "Todoist Agent"
    skills: list[AgentSkill] = []
    organization: str = "Todoist Agent"
    url: str = "http://localhost:10020"
