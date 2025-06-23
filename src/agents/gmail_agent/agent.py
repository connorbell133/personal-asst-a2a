"""Agent module."""

from pydantic_ai import Agent, RunContext

from src.mcp_handler.mcp_gmail import server
from dotenv import load_dotenv

load_dotenv(override=True)

agent = Agent(
    model="google-gla:gemini-2.5-flash",
    mcp_servers=[server],
    name="gmail_agent",
)


@agent.system_prompt
def review_agent_system_prompt(ctx: RunContext) -> str:
    """
    Returns the comprehensive system prompt for the AI-powered GitHub Pull Request review agent.

    The prompt provides detailed, step-by-step instructions for conducting a multi-phase PR review, including technical analysis, lint report evaluation, interactive feedback, risk assessment, and actionable review comment generation. It specifies the required comment format, outlines the use of available GitHub MCP tools, and defines the expected structure and tone for the agent's output. The prompt is dynamically populated with PR metadata from the provided context.
    """
    return """
You are a Gmail agent.
You are given a task to create a new email in Gmail.
You are also given a list of emails that are already in Gmail.
You are also given a list of emails that are already in Gmail.
"""


async def run_gmail_agent(task: str) -> str:
    async with agent.run_mcp_servers():
        result = await agent.run(
            task,
        )
        return result.output


app = agent.to_a2a()
