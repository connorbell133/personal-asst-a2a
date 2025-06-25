"""Agent Executor module."""

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.tasks import TaskUpdater
from a2a.types import Part, TaskState, TextPart
from a2a.utils import new_agent_text_message, new_task
from google.adk.artifacts import InMemoryArtifactService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from pydantic_ai import Agent


class PydanticAgentExecutor(AgentExecutor):
    def __init__(
        self,
        agent: Agent,
        status_message="Processing request...",
        artifact_name="response",
    ):
        """Initialize a generic ADK agent executor.

        Args:
            agent: The ADK agent instance
            status_message: Message to display while processing
            artifact_name: Name for the response artifact
        """
        self.agent = agent
        self.status_message = status_message
        self.artifact_name = artifact_name
        self.runner = Runner(
            app_name=agent.name,
            agent=agent,
            artifact_service=InMemoryArtifactService(),
            session_service=InMemorySessionService(),
            memory_service=InMemoryMemoryService(),
        )

    async def cancel(self, task_id: str) -> None:
        """
        Cancel the execution of the task identified by the given task ID.
        
        Parameters:
            task_id (str): The unique identifier of the task to cancel.
        """
        # Implementation for cancelling tasks

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        """
        Runs the agent asynchronously with the provided context and event queue, managing task lifecycle and status updates.
        
        The method retrieves user input, creates or retrieves a task, and enqueues it. It updates the task status to "working," executes the agent, captures the output, attaches it as an artifact, and marks the task as complete. If an exception occurs, the task status is set to "failed" and an error message is sent.
        """
        query = context.get_user_input()
        task = context.current_task or new_task(context.message)
        await event_queue.enqueue_event(task)
        updater = TaskUpdater(event_queue, task.id, task.contextId)
        try:
            await updater.update_status(
                TaskState.working,
                new_agent_text_message(self.status_message, task.contextId, task.id),
            )
            # Directly invoke the pydantic agent
            async with self.agent.run_mcp_servers():
                result = await self.agent.run(query)
            # Extract string output from result if needed
            response_text = result.output if hasattr(result, "output") else result
            await updater.add_artifact(
                [Part(root=TextPart(text=response_text))], name=self.artifact_name
            )
            await updater.complete()
        except Exception as e:
            await updater.update_status(
                TaskState.failed,
                new_agent_text_message(f"Error: {e!s}", task.contextId, task.id),
                final=True,
            )
