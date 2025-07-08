"""
This module contains the function to run dotenv-linter.

dotenv-linter is a tool that lints .env files.

Args:
    repo_path: The path to the repository.

Returns:
    dict: The output of the dotenv-linter command.
"""

import os
import shutil
from typing import Any

from core.cmd import run_command


def run_dotenv_linter(repo_path: str) -> dict[str, Any]:
    """
    Lints `.env` files in the specified repository directory using dotenv-linter.

    Parameters:
        repo_path (str): Path to the repository directory to search for `.env` files.

    Returns:
        dict[str, Any]: A dictionary containing the tool name and the output of the linter, or a skip message if no `.env` files are found.
    """
    tool_name = "dotenv-linter"

    # check if .env or .env.* file exists
    env_files = [f for f in os.listdir(repo_path) if f.startswith(".env")]
    if not env_files:
        return {"tool": tool_name, "skipped": True, "reason": "No .env file found."}

    # check if dotenv-linter is installed
    if not shutil.which("dotenv-linter"):
        run_command(["brew", "install", "dotenv-linter"], cwd=repo_path)

    cmd = ["dotenv-linter", repo_path]
    return {"tool": tool_name, **run_command(cmd, cwd=repo_path)}
