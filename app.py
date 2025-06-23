import time

import asyncio
from typing import Callable, Dict
from src.agents.gmail_agent import gmail_agent, GmailAgentCard
from src.agents.todoist_agent import todoist_agent, TodoistAgentCard
from src.agents.calendar_agent import calendar_agent, CalendarAgentCard
from src.agents.orchestration_agent import (
    personal_assistant_system_prompt,
    OrchestrationAgentCard,
)
from src.agents.common.tool_client import A2AToolClient
from src.agents.common.agent import run_agent_in_background
from src.agents.common.server import create_agent_a2a_server
from a2a.server.apps import A2AStarletteApplication
from pydantic_ai import Agent

a2a_client = A2AToolClient()


def create_gmail_agent_server(host="localhost", port=10020) -> A2AStarletteApplication:
    """Create A2A server for Gmail Agent using the unified wrapper."""
    return create_agent_a2a_server(
        agent=gmail_agent,
        name=GmailAgentCard.name,
        description=GmailAgentCard.description,
        skills=GmailAgentCard.skills,
        host=host,
        port=port,
        status_message="Searching for Gmail messages...",
        artifact_name="response",
    )


def create_todoist_agent_server(
    host="localhost", port=10021
) -> A2AStarletteApplication:
    """Create A2A server for Todoist Agent using the unified wrapper."""
    return create_agent_a2a_server(
        agent=todoist_agent,
        name=TodoistAgentCard.name,
        description=TodoistAgentCard.description,
        skills=TodoistAgentCard.skills,
        host=host,
        port=port,
        status_message="Searching for Todoist tasks...",
        artifact_name="response",
    )


def create_calendar_agent_server(
    host="localhost", port=10021
) -> A2AStarletteApplication:
    """Create A2A server for Calendar Agent using the unified wrapper."""
    return create_agent_a2a_server(
        agent=calendar_agent,
        name=CalendarAgentCard.name,
        description=CalendarAgentCard.description,
        skills=CalendarAgentCard.skills,
        host=host,
        port=port,
        status_message="Searching for Calendar events...",
        artifact_name="response",
    )


orchestration_agent = Agent(
    model="google-gla:gemini-2.5-pro",
    name="personal_assistant_agent",
    tools=[a2a_client.list_remote_agents, a2a_client.create_task],
    system_prompt=personal_assistant_system_prompt(),
)


def create_orchestration_agent_server(
    host="localhost", port=10021
) -> A2AStarletteApplication:
    """Create A2A server for Orchestration Agent using the unified wrapper."""
    return create_agent_a2a_server(
        agent=orchestration_agent,
        name=OrchestrationAgentCard.name,
        description=OrchestrationAgentCard.description,
        skills=OrchestrationAgentCard.skills,
        host=host,
        port=port,
        status_message="Searching for Calendar events...",
        artifact_name="response",
    )


agents: list[Dict[str, Callable[[str, int], A2AStarletteApplication]]] = [
    {
        "name": "Gmail Agent",
        "agent": create_gmail_agent_server,
        "port": 10020,
    },
    {
        "name": "Todoist Agent",
        "agent": create_todoist_agent_server,
        "port": 10022,
    },
    {
        "name": "Calendar Agent",
        "agent": create_calendar_agent_server,
        "port": 10023,
    },
    {
        "name": "Orchestration Agent",
        "agent": create_orchestration_agent_server,
        "port": 10024,
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
