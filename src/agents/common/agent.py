import asyncio
import threading

from src.agents.common.server import run_uvicorn_server


def run_agent_in_background(create_agent_function, port, name):
    """Run an agent server in a background thread."""

    def run() -> None:
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
