import asyncio
import time
import logfire
from a2a.server.apps import A2AStarletteApplication
from src.agents.common.agent import run_agent_in_background
from src.agents.common.server import create_agent_a2a_server
from src.agents.calendar_agent import CalendarAgentCard, calendar_agent
from src.agents.gmail_agent import GmailAgentCard, gmail_agent
from src.agents.orchestration_agent import (
    OrchestrationAgentCard,
    orchestration_agent,
    a2a_client,
)
from src.agents.todoist_agent import TodoistAgentCard, todoist_agent

# ---------------------------------------------------------------------------
# Configure Logfire for comprehensive observability. This will print a link
# to the local Logfire Live view and automatically display logs in the
# console. You can set LOGFIRE_TOKEN or other env vars to forward traces to
# the hosted Logfire backend if desired.
# ---------------------------------------------------------------------------

# Capture Pydantic-AI and HTTPX calls which power the agent runtime.
try:
    logfire.instrument_pydantic_ai()
except AttributeError:
    # Older versions of Logfire may not have this helper; skip gracefully.
    pass

try:
    logfire.instrument_httpx()
except AttributeError:
    pass


def create_gmail_agent_server() -> A2AStarletteApplication:
    """Create A2A server for Gmail Agent using the unified wrapper."""
    return create_agent_a2a_server(
        agent=gmail_agent,
        name=GmailAgentCard.name,
        description=GmailAgentCard.description,
        skills=GmailAgentCard.skills,
        host=GmailAgentCard.host,
        port=GmailAgentCard.port,
        status_message="Searching for Gmail messages...",
        artifact_name="response",
    )


def create_todoist_agent_server() -> A2AStarletteApplication:
    """Create A2A server for Todoist Agent using the unified wrapper."""
    return create_agent_a2a_server(
        agent=todoist_agent,
        name=TodoistAgentCard.name,
        description=TodoistAgentCard.description,
        skills=TodoistAgentCard.skills,
        host=TodoistAgentCard.host,
        port=TodoistAgentCard.port,
        status_message="Searching for Todoist tasks...",
        artifact_name="response",
    )


def create_calendar_agent_server() -> A2AStarletteApplication:
    """Create A2A server for Calendar Agent using the unified wrapper."""
    return create_agent_a2a_server(
        agent=calendar_agent,
        name=CalendarAgentCard.name,
        description=CalendarAgentCard.description,
        skills=CalendarAgentCard.skills,
        host=CalendarAgentCard.host,
        port=CalendarAgentCard.port,
        status_message="Searching for Calendar events...",
        artifact_name="response",
    )


def create_orchestration_agent_server() -> A2AStarletteApplication:
    """Create A2A server for Orchestration Agent using the unified wrapper."""
    return create_agent_a2a_server(
        agent=orchestration_agent,
        name=OrchestrationAgentCard.name,
        description=OrchestrationAgentCard.description,
        skills=OrchestrationAgentCard.skills,
        host=OrchestrationAgentCard.host,
        port=OrchestrationAgentCard.port,
        status_message="Searching for Calendar events...",
        artifact_name="response",
    )


agents = [
    {
        "name": GmailAgentCard.name,
        "agent": create_gmail_agent_server,
        "port": GmailAgentCard.port,
    },
    {
        "name": TodoistAgentCard.name,
        "agent": create_todoist_agent_server,
        "port": TodoistAgentCard.port,
    },
    {
        "name": CalendarAgentCard.name,
        "agent": create_calendar_agent_server,
        "port": CalendarAgentCard.port,
    },
    {
        "name": OrchestrationAgentCard.name,
        "agent": create_orchestration_agent_server,
        "port": OrchestrationAgentCard.port,
    },
]


# Start agent servers with corrected function calls
print("Starting agent servers...\n")

threads = []
for agent in agents:
    threads.append(
        run_agent_in_background(agent["agent"], agent["port"], agent["name"])
    )


# Wait for servers to start
time.sleep(3)

# Check if threads are alive
if all(thread.is_alive() for thread in threads):
    print("\n✅ Agent servers are running!")
    for agent in agents:
        print(f"   - {agent['name']}: http://127.0.0.1:{agent['port']}")
else:
    print("\n❌ Agent servers failed to start. Check the error messages above.")


for agent in agents:
    a2a_client.add_remote_agent(f"http://localhost:{agent['port']}")

remote_agents = a2a_client.list_remote_agents()
for k, v in remote_agents.items():
    print(f"Remote agent url: {k}")
    print(f"Remote agent name: {v['name']}")
    print(f"Remote agent skills: {v['skills']}")
    print(f"Remote agent version: {v['version']}")
    print("----\n")


async def main():
    trending_topics = await a2a_client.create_task(
        "http://localhost:10024", "has arda@getdelve.com sent me an email today?"
    )
    print(trending_topics)


asyncio.run(main())
