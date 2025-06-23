"""
This module contains the base class for the lint report.

Args:
    repo_path: The path to the repository.

Returns:
    LintReport: The lint report for the repository.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel

from . import (
    run_dotenv_linter,
    run_gitleaks,
    run_markdownlint,
    run_pylint,
    run_pytest,
    run_semgrep,
)


class LintReport(BaseModel):
    """
    This is a model that contains the lint report for the repository.
    """

    semgrep: dict[str, Any] | None = None
    gitleaks: dict[str, Any] | None = None
    dotenv_linter: dict[str, Any] | None = None
    markdownlint: dict[str, Any] | None = None
    pytest: dict[str, Any] | None = None
    pylint: dict[str, Any] | None = None


def lint_repo(repo_path: str) -> LintReport:
    """
    Runs multiple linters and test tools on the specified repository path and aggregates their results into a LintReport.

    Parameters:
        repo_path (str): Path to the repository to be analyzed.

    Returns:
        LintReport: An object containing the results from various linting and testing tools for the repository.
    """
    curr_report = LintReport()
    curr_report.semgrep = run_semgrep(repo_path)
    curr_report.gitleaks = run_gitleaks(repo_path)
    curr_report.dotenv_linter = run_dotenv_linter(repo_path)
    curr_report.markdownlint = run_markdownlint(repo_path)
    curr_report.pytest = run_pytest(repo_path)
    curr_report.pylint = run_pylint(repo_path)

    return curr_report
