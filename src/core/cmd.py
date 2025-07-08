"""
This module contains the function to run a command in a subprocess.

Args:
    command: The command to run.
    cwd: The current working directory.

Returns:
    dict: The output of the command.
"""

import subprocess
from typing import Any

from core.logger import logger


def run_command(command: list[str | int], cwd: str) -> dict[str, Any]:
    """
    Execute a shell command as a subprocess in a specified working directory.

    Parameters:
        command (list[str | int]): The command and its arguments to execute.
        cwd (str): The working directory in which to run the command.

    Returns:
        dict[str, Any]: A dictionary containing the executed command string, return code, standard output, standard error, and a success flag. If the command is not found or exits with a non-zero status, success is set to False and error details are included.
    """
    # Ensure every part of the command is a string for join/exec safety
    command_str_parts = [str(c) for c in command]
    logger.info("Executing command: `%s` in `%s`", " ".join(command_str_parts), cwd)
    try:
        completed = subprocess.run(
            command_str_parts,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True,  # Raise exception on non-zero exit codes
        )
        logger.info("Command succeeded.")
        return {
            "command": " ".join(command_str_parts),
            "returncode": completed.returncode,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
            "success": True,
        }
    except FileNotFoundError:
        logger.exception("Command not found: %s", command_str_parts[0])
        return {
            "command": " ".join(command_str_parts),
            "returncode": -1,
            "stdout": "",
            "stderr": (
                f"Error: Command '{command_str_parts[0]}' not found. "
                "Is it installed and in the system's PATH?"
            ),
            "success": False,
        }
    except subprocess.CalledProcessError as e:
        # This is expected for linting/testing failures
        logger.warning("Command failed with exit code %d.", e.returncode)
        return {
            "command": " ".join(command_str_parts),
            "returncode": e.returncode,
            "stdout": e.stdout,
            "stderr": e.stderr,
            "success": False,
        }
