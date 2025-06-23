from a2a.types import AgentSkill


class OrchestrationAgentCard:
    name: str = "Orchestration Agent"
    description: str = "Orchestration Agent"
    skills: list[AgentSkill] = []
    organization: str = "Orchestration Agent"
    url: str = "http://localhost:10020"
