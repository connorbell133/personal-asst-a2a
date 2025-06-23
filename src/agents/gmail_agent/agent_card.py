from a2a.types import AgentSkill


class GmailAgentCard:
    name: str = "Gmail Agent"
    description: str = "Gmail Agent"
    skills: list[AgentSkill] = []
    organization: str = "Gmail Agent"
    url: str = "http://localhost:10020"
