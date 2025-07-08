"""
This module contains the function to run Semgrep.

Semgrep is a tool that scans code for security vulnerabilities.

Args:
    repo_path: The path to the repository.

Returns:
    dict: The output of the Semgrep command.
"""

from typing import Any

from core.cmd import run_command


def run_semgrep(repo_path: str) -> dict[str, Any]:
    """
    Run the Semgrep security scanner on the specified repository path.

    Parameters:
        repo_path (str): Path to the repository to be scanned.

    Returns:
        dict[str, Any]: A dictionary containing the tool name and the results from the Semgrep scan.
    """
    tool_name = "semgrep"
    cmd = ["semgrep", "scan", repo_path]
    return {"tool": tool_name, **run_command(cmd, cwd=repo_path)}
