"""
This module contains the function to run Ruff.

Ruff is a tool that lints Python code.

Args:
    repo_path: The path to the repository.

Returns:
    dict: The output of the Ruff command.
"""

import os
from typing import Any

from core.cmd import run_command
from core.logger import logger


# COMPLETE :: NOT TESTED
def run_ruff(
    repo_path: str, fix: bool = False, request_action: bool = False
) -> dict[str, Any]:
    """
    Run the Ruff linter on a Python repository and return the results.

    Attempts to install Ruff in the specified repository directory to ensure it is available. Detects Ruff configuration files and constructs the appropriate lint command. If installation fails, returns a result indicating the tool was skipped. Optionally includes a message prompting a fix action if requested.

    Parameters:
        repo_path (str): Path to the root of the Python repository to lint.
        fix (bool, optional): If True, applies automatic fixes using Ruff. Defaults to False.
        request_action (bool, optional): If True, includes a message prompting a fix action in the result. Defaults to False.

    Returns:
        dict[str, Any]: A dictionary containing the tool name and the results of the Ruff lint command, or a skip reason if Ruff could not be installed.
    """

    tool_name = "ruff"

    # Ensure Ruff is installed so the command can run in ephemeral environments
    install_result = run_command(["pip", "install", "ruff"], cwd=repo_path)
    if install_result["returncode"] != 0:
        logger.error("Failed to install Ruff.")
        return {
            "tool": tool_name,
            "skipped": True,
            "reason": "Failed to install Ruff.",
        }
    if os.path.exists(os.path.join(repo_path, "pyproject.toml")):
        config_file = os.path.join(repo_path, "pyproject.toml")
    elif os.path.exists(os.path.join(repo_path, "ruff.toml")):
        config_file = os.path.join(repo_path, "ruff.toml")
    else:
        config_file = None
    # If no Ruff configuration is detected, skip execution to avoid noisy
    # output
    base_command = ["ruff", "check", "--show-files"]
    if fix:
        base_command.append("--fix")
    if config_file:
        base_command.append("--config")
        base_command.append(config_file)

    lint_result = run_command(base_command, cwd=repo_path)
    if request_action:
        message = """
Looks like ruff found some issues in the repository: reply '@repo-sage ruff' to fix them.
"""
        return {"tool": tool_name, "message": message, **lint_result}
    return {"tool": tool_name, **lint_result}
