"""
This module contains the MCP server for the GitHub Helper project.

Args:
    None

Returns:
    server: The MCP server for the GitHub Helper project.
"""

from pydantic_ai.mcp import MCPServerStdio

server = MCPServerStdio(
    command="npx",
    args=[
        "--yes",
        "@gongrzhe/server-gmail-autoauth-mcp",
    ],
    env={"GOOGLE_OAUTH_CREDENTIALS": "/Users/connor/assistant/gcp-oauth.keys.json"},
)
