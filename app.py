import asyncio
import json
import time
import logfire
import requests

import uvicorn
from fastapi import FastAPI, Request
from src.agents import (
    run_agent_in_background,
    agent_manager,
    CalendarAgentCard,
    calendar_agent,
    GmailAgentCard,
    gmail_agent,
    ObsidianAgentCard,
    obsidian_agent,
    OrchestrationAgentCard,
    orchestration_agent,
    a2a_client,
    TodoistAgentCard,
    todoist_agent,
)


# ---------------------------------------------------------------------------
# Configure Logfire as early as possible so that all subsequent imports
# (including HTTPX, Pydantic-AI, etc.) are captured. If LOGFIRE_TOKEN is set
# the data will be sent to Logfire Cloud; otherwise logs are printed locally.
# ---------------------------------------------------------------------------

try:
    # Don't error if already configured elsewhere (e.g. via tests)
    if not getattr(logfire, "_configured", False):  # type: ignore[attr-defined]
        logfire.configure(send_to_logfire="if-token-present")
except Exception as e:  # pragma: no cover – best-effort setup
    print(f"[Logfire] Failed to configure Logfire: {e!s}")

try:
    logfire.instrument_pydantic_ai()
except AttributeError:
    # Older versions of Logfire may not have this helper; skip gracefully.
    pass

try:
    logfire.instrument_httpx()
except AttributeError:
    pass


def register_all_agents():
    """Register all agents with the agent manager."""

    # Register Gmail agent
    agent_manager.register_agent(
        name=GmailAgentCard.name,
        card_class=GmailAgentCard,
        agent_instance=gmail_agent,
        status_message="Searching for Gmail messages...",
    )

    # Register Todoist agent
    agent_manager.register_agent(
        name=TodoistAgentCard.name,
        card_class=TodoistAgentCard,
        agent_instance=todoist_agent,
        status_message="Searching for Todoist tasks...",
    )

    # Register Calendar agent
    agent_manager.register_agent(
        name=CalendarAgentCard.name,
        card_class=CalendarAgentCard,
        agent_instance=calendar_agent,
        status_message="Searching for Calendar events...",
    )

    # Register Obsidian agent
    agent_manager.register_agent(
        name=ObsidianAgentCard.name,
        card_class=ObsidianAgentCard,
        agent_instance=obsidian_agent,
        status_message="Managing Obsidian vault...",
    )

    # Register Orchestration agent
    agent_manager.register_agent(
        name=OrchestrationAgentCard.name,
        card_class=OrchestrationAgentCard,
        agent_instance=orchestration_agent,
        status_message="Orchestrating agents...",
    )


def main():
    """Main application entry point."""

    # Register all agents
    register_all_agents()

    # Get agent list from manager
    agents = agent_manager.get_agent_list()

    # Start agent servers
    print("Starting agent servers...\n")

    threads = []
    for agent in agents:
        threads.append(
            run_agent_in_background(agent["agent"], agent["port"], agent["name"])
        )

    # Wait for servers to become healthy
    max_wait = 30  # seconds
    start_time = time.time()

    while time.time() - start_time < max_wait:
        if all(thread.is_alive() for thread in threads):
            # Additional health check: try to reach agent endpoints
            all_healthy = True
            for agent in agents:
                try:
                    response = requests.get(
                        f"http://localhost:{agent['port']}/.well-known/agent.json",
                        timeout=1,
                    )
                    if response.status_code != 200:
                        all_healthy = False
                        break
                except Exception as e:
                    print(f"Error checking agent health: {e}")
                    all_healthy = False
                    break

            if all_healthy:
                break

        time.sleep(0.5)

    # Check if threads are alive
    if all(thread.is_alive() for thread in threads):
        print("\n✅ Agent servers are running!")
        for agent in agents:
            print(f"   - {agent['name']}: http://127.0.0.1:{agent['port']}")
    else:
        print("\n❌ Agent servers failed to start. Check the error messages above.")

    # Register remote agents
    for agent in agents:
        a2a_client.add_remote_agent(f"http://localhost:{agent['port']}")

    # Display remote agent info
    remote_agents = a2a_client.list_remote_agents()
    for k, v in remote_agents.items():
        print(f"Remote agent url: {k}")
        print(f"Remote agent name: {v['name']}")
        print(f"Remote agent skills: {v['skills']}")
        print(f"Remote agent version: {v['version']}")
        print("----\n")


async def test_agent():
    """Test agent functionality."""
    # Query the Gmail Agent that is started above (running on port 10021)
    while True:
        user_input = input("Enter a task: ")
        trending_topics = await a2a_client.create_task(
            "http://localhost:10021",
            user_input,
        )
        print(trending_topics)


app = FastAPI()


@app.get("/test")
async def root():
    return {"message": "Hello, World!"}


@app.post("/agent/orchestration/create_task")
async def orchestration_create_task(request: Request):
    body = await request.json()
    print(body)

    try:
        trending_topics = await a2a_client.create_task(
            "http://localhost:10021",
            body["user_input"],
        )

        # Handle empty or invalid JSON responses
        if not trending_topics or trending_topics.strip() == "":
            return {"message": "No response received from agent"}

        # Try to parse as JSON, but handle cases where it's already a string
        try:
            parsed_response = json.loads(trending_topics)
            return {"message": parsed_response}
        except json.JSONDecodeError:
            # If it's not valid JSON, return the raw response
            return {"message": trending_topics}

    except Exception as e:
        # Handle any other errors from the agent communication
        return {"message": f"Error communicating with agent: {str(e)}"}


# Ensure asyncio child watcher is set to avoid NotImplementedError when spawning subprocesses in threads
if hasattr(asyncio, "ThreadedChildWatcher"):
    try:
        asyncio.get_event_loop_policy().set_child_watcher(
            asyncio.ThreadedChildWatcher()
        )
    except NotImplementedError:
        # Some platforms may not support setting a child watcher (e.g., Windows Proactor loop)
        pass


if __name__ == "__main__":
    main()
    uvicorn.run(app, host="0.0.0.0", port=8000)
