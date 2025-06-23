"""
This module contains the function to run Pylint.

Pylint is a tool that lints Python code.

Args:
    repo_path: The path to the repository.

Returns:
    dict: The output of the Pylint command.
"""

import os
from typing import Any

from core.cmd import run_command


def run_pylint(repo_path: str) -> dict[str, Any]:
    """
    Run Pylint on the specified repository path using an available configuration file.

    Checks for a `pylint.rc` or `pyproject.toml` file in the repository directory and uses it as the Pylint configuration if found. Returns a dictionary containing the tool name and the results of the Pylint execution.

    Parameters:
        repo_path (str): Path to the repository to be linted.

    Returns:
        dict[str, Any]: Dictionary with the tool name and the result of the Pylint command.
    """
    tool_name = "pylint"

    if os.path.exists(os.path.join(repo_path, "pylint.rc")):
        config_file = os.path.join(repo_path, "pylint.rc")
    elif os.path.exists(os.path.join(repo_path, "pyproject.toml")):
        config_file = os.path.join(repo_path, "pyproject.toml")
    else:
        config_file = None

    base_command = ["pylint", repo_path]
    if config_file:
        base_command.append("--config")
        base_command.append(config_file)

    lint_result = run_command(base_command, cwd=repo_path)
    return {"tool": tool_name, **lint_result}
