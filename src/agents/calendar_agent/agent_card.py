"""Agent Card module."""

from pydantic import BaseModel
from a2a.types import AgentSkill


class CalendarAgentCard(BaseModel):
    """
    Calendar Agent Card.
    """

    name: str = "Calendar Agent"
    description: str = "Calendar Agent"
    skills: list[AgentSkill] = []
    organization: str = "Calendar Agent"
    url: str = "http://localhost:10020"
