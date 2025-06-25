"""Agent Card module."""

from pydantic import BaseModel
from a2a.types import AgentSkill


class GmailAgentCard(BaseModel):
    """
    Gmail Agent Card.
    """

    name: str = "Gmail Agent"
    description: str = "Gmail Agent"
    skills: list[AgentSkill] = []
    organization: str = "Gmail Agent"
    url: str = "http://localhost:10020"
