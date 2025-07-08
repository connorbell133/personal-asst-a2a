"""Agent module."""

from pydantic_ai import Agent, RunContext
from dotenv import load_dotenv
import logfire

from src.mcp_handler.mcp_gmail import server
from .tools import (
    get_github_folder_contents,
    print_folder_tree,
    get_github_file_contents,
    send_new_content_to_github,
    delete_note_from_github,
)

load_dotenv(override=True)

agent = Agent(
    model="google-gla:gemini-2.5-flash",
    mcp_servers=[server],
    name="obsidian_agent",
)


@agent.system_prompt
def review_agent_system_prompt(ctx: RunContext) -> str:
    """
    Returns the comprehensive system prompt for the AI-powered GitHub Pull Request review agent.

    The prompt provides detailed, step-by-step instructions for conducting a multi-phase PR review, including technical analysis, lint report evaluation, interactive feedback, risk assessment, and actionable review comment generation. It specifies the required comment format, outlines the use of available GitHub MCP tools, and defines the expected structure and tone for the agent's output. The prompt is dynamically populated with PR metadata from the provided context.
    """
    return """

"""


async def run_obsidian_agent(task: str) -> str:
    async with agent.run_mcp_servers():
        result = await agent.run(
            task,
        )
        return result.output


@agent.tool
def list_folder_tree(
    ctx: RunContext,
    folder: str = "meetings",
    owner: str = "connorbell133",
    repo: str = "obsidian",
) -> dict:
    """List the folder tree of the given folder."""
    # Make sure to set your GITHUB_TOKEN environment variable
    if ctx.deps.GITHUB_TOKEN:
        logfire.debug(f"Listing contents of '{folder}' in '{owner}/{repo}':")
        repo_tree = get_github_folder_contents(owner, repo, folder)

        if repo_tree:
            return {
                "success": True,
                "folder_tree": print_folder_tree(repo_tree),
            }
        else:
            return {
                "success": False,
                "error": "Could not retrieve folder tree.",
            }
    else:
        return {
            "success": False,
            "error": "GITHUB_TOKEN environment variable not set. Please set it before running.",
        }


@agent.tool
def create_note(
    ctx: RunContext,
    note_path: str,
    content: str,
    owner: str = "connorbell133",
    repo: str = "obsidian",
) -> dict:
    """Create a new note."""
    # create the note
    response = send_new_content_to_github(note_path, content, owner, repo)

    return response


@agent.tool
def read_note(
    ctx: RunContext,
    note_path: str,
    owner: str = "connorbell133",
    repo: str = "obsidian",
) -> dict:
    """Get the content of the given note."""
    return get_github_file_contents(owner, repo, note_path)


@agent.tool
def update_note(
    ctx: RunContext,
    note_path: str,
    content: str,
    owner: str = "connorbell133",
    repo: str = "obsidian",
) -> dict:
    """Update the content of the given note."""
    # get the note content
    note_content = read_note(note_path, owner, repo)
    if not note_content["success"]:
        return note_content

    # update the note content
    new_content = {
        "success": True,
        "file_contents": note_content["file_contents"] + content,
    }

    # send new content to github
    response = send_new_content_to_github(
        note_path, new_content["file_contents"], owner, repo
    )

    return response


@agent.tool
def delete_note(
    ctx: RunContext,
    note_path: str,
    owner: str = "connorbell133",
    repo: str = "obsidian",
) -> dict:
    """Delete the given note."""
    return delete_note_from_github(note_path, owner, repo)


app = agent.to_a2a()
