"""Agent module."""

from pydantic_ai import Agent, RunContext

from src.mcp_handler.mcp_gcal import server
from dotenv import load_dotenv

load_dotenv(override=True)

agent = Agent(
    model="google-gla:gemini-2.5-flash",
    mcp_servers=[server],
)


@agent.system_prompt
def review_agent_system_prompt(ctx: RunContext) -> str:
    """
    Returns the comprehensive system prompt for the AI-powered GitHub Pull Request review agent.

    The prompt provides detailed, step-by-step instructions for conducting a multi-phase PR review, including technical analysis, lint report evaluation, interactive feedback, risk assessment, and actionable review comment generation. It specifies the required comment format, outlines the use of available GitHub MCP tools, and defines the expected structure and tone for the agent's output. The prompt is dynamically populated with PR metadata from the provided context.
    """
    return """
You are a Google Calendar agent.
You are given a task to create a new event in Google Calendar.
You are also given a list of events that are already in Google Calendar.
You are also given a list of events that are already in Google Calendar.
"""


async def run_calendar_agent(task: str) -> str:
    async with agent.run_mcp_servers():
        result = await agent.run(
            task,
        )
        return result.output


app = agent.to_a2a()
