"""Agent module."""

import asyncio
import threading

from src.agents.common.server import run_uvicorn_server


def run_agent_in_background(create_agent_function, port, name):
    """
    Starts an agent server in a background daemon thread.

    The agent server is created using the provided factory function and runs asynchronously on the specified port. Any exceptions during server execution are printed with the agent's name.

    Parameters:
        create_agent_function: A callable that returns the agent instance to be served.
        port (int): The port number on which the server will listen.
        name (str): The name of the agent, used for error reporting.

    Returns:
        threading.Thread: The background thread running the agent server.
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
