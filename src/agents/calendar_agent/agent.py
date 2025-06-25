"""Agent module."""

from dotenv import load_dotenv
from pydantic_ai import Agent, RunContext

from src.mcp_handler.mcp_gcal import server as calendar_server

load_dotenv(override=True)

calendar_agent = Agent(
    model="google-gla:gemini-2.5-flash",
    mcp_servers=[calendar_server],
)


@calendar_agent.system_prompt
def review_agent_system_prompt(ctx: RunContext) -> str:
    """
    Returns the comprehensive system prompt for the AI-powered GitHub Pull Request review agent.
    """
    return """
You are a Google Calendar agent.
You are given a task to create a new event in Google Calendar.
You are also given a list of events that are already in Google Calendar.
You are also given a list of events that are already in Google Calendar.
"""


async def run_calendar_agent(task: str) -> str:
    """Run Calendar Agent function."""
    async with calendar_agent.run_mcp_servers():
        result = await calendar_agent.run(
            task,
        )
        return result.output


app = calendar_agent.to_a2a()
