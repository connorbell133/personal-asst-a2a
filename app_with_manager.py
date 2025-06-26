import asyncio
import time
import logfire
import requests

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
                except:
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
    trending_topics = await a2a_client.create_task(
        "http://localhost:10021",
        "has arda@getdelve.com sent me an email today?",
    )
    print(trending_topics)


if __name__ == "__main__":
    main()
    asyncio.run(test_agent())
