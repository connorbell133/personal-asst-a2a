"""
This module contains the function to run markdownlint.

markdownlint is a tool that lints Markdown files.

Args:
    repo_path: The path to the repository.

Returns:
    dict: The output of the markdownlint command.
"""

import os
import shutil
from typing import Any

from core.cmd import run_command


def run_markdownlint(repo_path: str) -> dict[str, Any]:
    """
    Executes markdownlint on all Markdown files in the specified repository directory.

    If no Markdown files are found, returns a result indicating the linting was skipped. Installs markdownlint locally using npm if it is not already available. Returns a dictionary containing the tool name and the output from the linting process.

    Parameters:
        repo_path (str): Path to the repository directory to lint.

    Returns:
        dict[str, Any]: A dictionary with the tool name, and either the linting results or a skip reason.
    """
    tool_name = "markdownlint"
    # check for markdown files
    markdown_files = [f for f in os.listdir(repo_path) if f.endswith(".md")]
    if not markdown_files:
        return {
            "tool": tool_name,
            "skipped": True,
            "reason": "No markdown files found.",
        }

    # check if markdownlint is installed
    if not shutil.which("markdownlint"):
        run_command(["npm", "install", "markdownlint", "--save-dev"], cwd=repo_path)

    cmd = ["markdownlint", "directories", repo_path]
    return {"tool": tool_name, **run_command(cmd, cwd=repo_path)}
