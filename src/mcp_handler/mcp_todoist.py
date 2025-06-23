"""
This module contains the MCP server for the GitHub Helper project.

Args:
    None

Returns:
    server: The MCP server for the GitHub Helper project.
"""

import os

from dotenv import load_dotenv
from pydantic_ai.mcp import MCPServerStdio

load_dotenv()
token = os.getenv("TODOIST_API_TOKEN")
if not token:
    raise ValueError("Set TODOIST_API_TOKEN in your env/.env file")

server = MCPServerStdio(
    command="npx",
    args=[
        "--yes",
        "@abhiz123/todoist-mcp-server",
    ],
    env={"TODOIST_API_TOKEN": token},
)
