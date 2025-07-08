"""
This module contains the MCP server for the Todoist integration.

Args:
    None

Returns:
    server: The MCP server for the Todoist integration.
"""

import os
import warnings

from dotenv import load_dotenv
from pydantic_ai.mcp import MCPServerStdio

load_dotenv()
token = os.getenv("TODOIST_API_TOKEN")

# Create server only if token is available
if token:
    server = MCPServerStdio(
        command="npx",
        args=[
            "--yes",
            "@abhiz123/todoist-mcp-server",
        ],
        env={"TODOIST_API_TOKEN": token},
    )
else:
    warnings.warn(
        "TODOIST_API_TOKEN not found. Todoist MCP server will be unavailable."
    )
