import asyncio
import httpx
import uuid
from a2a.client import A2AClient
from a2a.types import (
    SendMessageRequest,
    Message,
    TextPart,
    Role,
    MessageSendParams,
    Task,
)
from src.agents.common.agent import (
    load_agent_config,
)  # Assuming this function is available for client-side too
from dotenv import load_dotenv

load_dotenv(override=True)

# Load the same config used for the agent to get its host and port
orchestration_agent_config = load_agent_config(
    "src/agents/orchestration_agent/config.yml"
)

# Define the agent's base URL
AGENT_BASE_URL = (
    f"http://{orchestration_agent_config.host}:{orchestration_agent_config.port}"
)


async def converse_with_agent():
    """
    Initiates a turn-based conversation with the Orchestration Agent.
    """
    # Configure timeout for longer orchestration requests
    timeout_config = httpx.Timeout(timeout=60.0, connect=10.0, read=60.0)
    async with httpx.AsyncClient(timeout=timeout_config) as http_client:
        try:
            # 1. Get the Agent Card and initialize the A2AClient
            print(f"Connecting to agent at: {AGENT_BASE_URL}")
            a2a_client = await A2AClient.get_client_from_agent_card_url(
                http_client, AGENT_BASE_URL
            )
            print("Successfully connected to the agent.")

            task_id = None  # To store the task ID for continuity

            print("\n--- Start Conversation ---")
            while True:
                user_input = input("You: ")
                if user_input.lower() in ["exit", "quit"]:
                    print("Exiting conversation.")
                    break

                # Create a text message object
                user_message = Message(
                    kind="message",
                    role=Role.user,
                    parts=[TextPart(text=user_input)],
                    taskId=task_id,  # Include taskId for ongoing conversation
                    messageId=str(uuid.uuid4()),  # Add messageId
                )

                # Create the SendMessageRequest
                send_request = SendMessageRequest(
                    id=str(uuid.uuid4()),  # Add request ID
                    params=MessageSendParams(
                        message=user_message,
                    ),
                )

                # 2. Send the message (using non-streaming for now)
                print("Agent (thinking...):")
                response = await a2a_client.send_message(send_request)

                # Handle the response - the actual result is in response.root.result
                if hasattr(response, "root") and hasattr(response.root, "result"):
                    result = response.root.result

                    if isinstance(result, Task):
                        # The response is a Task object
                        task = result
                        task_id = task.id  # Store the task ID for future turns
                        print(
                            f"  Task ID: {task.id}, Status: {task.status.state.value}"
                        )
                        if task.status.message:
                            print(f"  Task Message: {task.status.message}")

                        # Check for artifacts with response content
                        if task.artifacts:
                            for artifact in task.artifacts:
                                if artifact.parts:
                                    for part in artifact.parts:
                                        if hasattr(part, "root") and isinstance(
                                            part.root, TextPart
                                        ):
                                            print(f"  Agent: {part.root.text}")

                    elif isinstance(result, Message):
                        # The agent's actual message response
                        agent_message = result
                        for part in agent_message.parts:
                            if isinstance(part, TextPart):
                                print(f"  Agent: {part.text}")
                    else:
                        print(f"  Received response type: {type(result)}")
                else:
                    print(f"  Unexpected response structure: {response}")

        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    asyncio.run(converse_with_agent())
