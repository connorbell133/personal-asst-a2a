import asyncio
import threading

import uvicorn

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard
from pydantic_ai import Agent
from src.agents.common.agent_executor import PydanticAgentExecutor

servers = []


def create_agent_a2a_server(
    agent: Agent,
    name,
    description,
    skills,
    host="localhost",
    port=10020,
    status_message="Processing request...",
    artifact_name="response",
):
    """Create an A2A server for any ADK agent.

    Args:
        agent: The ADK agent instance
        name: Display name for the agent
        description: Agent description
        skills: List of AgentSkill objects
        host: Server host
        port: Server port
        status_message: Message shown while processing
        artifact_name: Name for response artifacts

    Returns:
        A2AStarletteApplication instance
    """
    # Agent capabilities
    capabilities = AgentCapabilities(streaming=True)

    # Agent card (metadata)
    agent_card = AgentCard(
        name=name,
        description=description,
        url=f"http://{host}:{port}/",
        version="1.0.0",
        defaultInputModes=["text", "text/plain"],
        defaultOutputModes=["text", "text/plain"],
        capabilities=capabilities,
        skills=skills,
    )

    # Create executor with custom parameters
    executor = PydanticAgentExecutor(
        agent=agent, status_message=status_message, artifact_name=artifact_name
    )

    request_handler = DefaultRequestHandler(
        agent_executor=executor,
        task_store=InMemoryTaskStore(),
    )

    # Create A2A application
    return A2AStarletteApplication(agent_card=agent_card, http_handler=request_handler)


async def run_uvicorn_server(create_agent_function, port):
    """Run server with proper error handling."""
    try:
        print(f"🚀 Starting agent on port {port}...")
        app = create_agent_function(port=port)
        config = uvicorn.Config(
            app.build(), host="127.0.0.1", port=port, log_level="error", loop="asyncio"
        )
        server = uvicorn.Server(config)
        servers.append(server)
        await server.serve()
    except Exception as e:
        print(f"Agent error: {e}")


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
