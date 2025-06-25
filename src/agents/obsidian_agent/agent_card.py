from a2a.types import AgentSkill


class ObsidianAgentCard:
    """
    This agent is used to manage the Obsidian vault.
    """

    name: str = "Obsidian Agent"
    description: str = "Obsidian Agent"
    skills: list[AgentSkill] = []
    organization: str = "Obsidian Agent"
    url: str = "http://localhost:10019"
