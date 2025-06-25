"""Agent module."""

from dotenv import load_dotenv
from pydantic_ai import Agent, RunContext

from src.mcp_handler.mcp_gmail import server as gmail_server

load_dotenv(override=True)

gmail_agent = Agent(
    model="google-gla:gemini-2.5-flash",
    mcp_servers=[gmail_server],
    name="gmail_agent",
)


@gmail_agent.system_prompt
def review_agent_system_prompt(ctx: RunContext) -> str:
    """
    Returns the comprehensive system prompt for the AI-powered GitHub Pull Request review agent.
    """
    return """
You are a Gmail agent.
You are given a task to create a new email in Gmail.
You are also given a list of emails that are already in Gmail.
You are also given a list of emails that are already in Gmail.
"""


async def run_gmail_agent(task: str) -> str:
    """Run Gmail Agent function."""
    async with gmail_agent.run_mcp_servers():
        result = await gmail_agent.run(
            task,
        )
        return result.output


app = gmail_agent.to_a2a()
