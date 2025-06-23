from a2a.types import AgentSkill


class TodoistAgentCard:
    name: str = "Todoist Agent"
    description: str = "Todoist Agent"
    skills: list[AgentSkill] = []
    organization: str = "Todoist Agent"
    url: str = "http://localhost:10020"
