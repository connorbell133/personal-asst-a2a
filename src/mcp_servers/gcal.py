"""
This module contains the MCP server for the GitHub Helper project.

Args:
    None

Returns:
    server: The MCP server for the GitHub Helper project.
"""

from pydantic_ai.mcp import MCPServerStreamableHTTP

server = MCPServerStreamableHTTP(url="http://host.docker.internal:8001/mcp")
