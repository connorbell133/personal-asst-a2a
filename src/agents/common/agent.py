"""Agent module."""

import asyncio
import threading
import yaml
from pydantic import BaseModel, ValidationError
from src.agents.common.server import run_uvicorn_server


class BaseAgentConfig(BaseModel):
    """
    Base agent config.
    """

    name: str
    description: str
    model: str
    system_prompt: str
    port: int
    host: str = "localhost"


def load_agent_config(config_path: str) -> BaseAgentConfig:
    """
    Load and validate an agent configuration from a YAML file.

    Parameters:
        config_path (str): Path to the YAML configuration file.

    Returns:
        BaseAgentConfig: An instance of BaseAgentConfig populated with the loaded configuration.

    Raises:
        ValueError: If the configuration file is invalid or fails schema validation.
        FileNotFoundError: If the configuration file does not exist.
    """
    agent_config = None
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            agent_config = yaml.safe_load(f)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Config file not found: {config_path}") from e
    try:
        return BaseAgentConfig(**agent_config)
    except ValidationError as e:
        raise ValueError(f"Error loading agent config: {e}") from e


def run_agent_in_background(create_agent_function, port, name):
    """
    Launches an agent server in a background daemon thread.

    Creates and starts a daemon thread that runs the agent server asynchronously on the specified port using the provided factory function. Any exceptions during server execution are printed with the agent's name.

    Returns:
        threading.Thread: The daemon thread running the agent server.
    """

    def run() -> None:
        """
        Starts a new asyncio event loop and runs the agent server coroutine until completion.

        Handles any exceptions raised during server execution by printing an error message with the agent's name.
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            # Create the coroutine inside the new event loop
            loop.run_until_complete(run_uvicorn_server(create_agent_function, port))
        except Exception as e:
            print(f"{name} error: {e}")

    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    return thread
