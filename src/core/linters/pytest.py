"""
This module contains the function to run Pytest.

Pytest is a tool that runs tests.

Args:
    repo_path: The path to the repository.

Returns:
    dict: The output of the Pytest command.
"""

import os
from typing import Any

from core.cmd import run_command


def run_pytest(repo_path: str) -> dict[str, Any]:
    """
    Run Pytest tests in the specified repository if a configuration file is present.

    Checks for the existence of either `pyproject.toml` or `pytest.ini` in the given repository path. If neither is found, returns a dictionary indicating the Pytest run was skipped and the reason. If a `requirements.txt` file exists, installs dependencies before running Pytest. Returns a dictionary containing the tool name and the result of the Pytest execution or skip information.

    Parameters:
        repo_path (str): Path to the repository directory to run Pytest in.

    Returns:
        dict[str, Any]: Dictionary with the tool name and either the Pytest execution result or skip details.
    """
    tool_name = "pytest"
    if not (
        os.path.exists(os.path.join(repo_path, "pyproject.toml"))
        or os.path.exists(os.path.join(repo_path, "pytest.ini"))
    ):
        return {"tool": tool_name, "skipped": True, "reason": "No config file found."}

    # Example: First install dependencies, then run tests
    # This is a simplified example. A real-world case might need `pip install
    # -r requirements.txt`
    if os.path.exists(os.path.join(repo_path, "requirements.txt")):
        run_command(["pip", "install", "-r", "requirements.txt"], cwd=repo_path)

    result = run_command(["pytest"], cwd=repo_path)
    return {"tool": tool_name, **result}
