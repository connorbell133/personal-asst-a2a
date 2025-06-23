"""
This module contains the function to run Gitleaks.

Gitleaks is a tool that scans the repository for secrets.

Args:
    repo_path: The path to the repository.
    config_file: The path to the Gitleaks configuration file.

Returns:
    dict: The output of the Gitleaks command.
"""

from typing import Any

from core.cmd import run_command


def run_gitleaks(repo_path: str, config_file: str | None = None) -> dict[str, Any]:
    """
    Scan a repository directory for secrets using Gitleaks.

    Parameters:
        repo_path (str): Path to the repository directory to scan.
        config_file (str, optional): Path to a Gitleaks configuration file to use for the scan.

    Returns:
        dict[str, Any]: A dictionary containing the results of the Gitleaks scan, including the tool name and output details.
    """
    cmd = ["gitleaks", "dir", repo_path, "--redact=20", "-v"]
    if config_file:
        cmd.append("--config-file")
        cmd.append(config_file)

    lint_result = run_command(cmd, cwd=repo_path)
    return {"tool": "gitleaks", **lint_result}
