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

# Project-wide logger
from src.core.logger import logger


# Helper to safely convert possibly large strings to a shorter preview for logs
def _preview(text: str, max_len: int = 200) -> str:
    """Return a shortened preview of *text* for log messages."""
    return text if len(text) <= max_len else text[:max_len] + "…"


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
        logger.debug("[Executor] Received user query: %s", _preview(query))

        task = context.current_task or new_task(context.message)
        logger.debug(
            "[Executor] Created/Retrieved task with id=%s context=%s",
            task.id,
            task.contextId,
        )

        await event_queue.enqueue_event(task)
        updater = TaskUpdater(event_queue, task.id, task.contextId)
        try:
            await updater.update_status(
                TaskState.working,
                new_agent_text_message(self.status_message, task.contextId, task.id),
            )
            logger.debug(
                "[Executor] Starting MCP servers for agent '%s'", self.agent.name
            )

            # ------------------------------------------------------------------
            # Starting MCP servers can raise a NotImplementedError when executed
            # from a background thread. This happens because asyncio's child
            # watcher API (used under the hood by Pydantic-AI to spawn
            # subprocesses) is only fully supported in the main thread on
            # Unix-like systems. When we run our agents in background *threads*
            # (not separate processes), hitting this path would crash the task
            # with:
            #   NotImplementedError: get_child_watcher
            #
            # To keep the system running we fall back to executing the agent
            # without spinning up the MCP servers when we detect this situation.
            # ------------------------------------------------------------------

            try:
                async with self.agent.run_mcp_servers():
                    logger.debug(
                        "[Executor] MCP servers running. Invoking agent '%s'",
                        self.agent.name,
                    )
                    result = await self.agent.run(query)
            except NotImplementedError as ne:
                logger.warning(
                    "[Executor] MCP servers unavailable in this context (likely"
                    " due to background thread). Proceeding without MCP servers: %s",
                    ne,
                )
                # Fallback: run the agent directly.
                result = await self.agent.run(query)

            # Extract string output from result if needed
            response_text = result.output if hasattr(result, "output") else result
            logger.debug(
                "[Executor] Agent '%s' returned response preview: %s",
                self.agent.name,
                _preview(str(response_text)),
            )
            await updater.add_artifact(
                [Part(root=TextPart(text=response_text))], name=self.artifact_name
            )
            logger.debug(
                "[Executor] Response artifact added and task completed successfully for task %s",
                task.id,
            )
            await updater.complete()
        except Exception as e:
            import traceback

            tb_str = traceback.format_exc()
            logger.error(
                "[Executor] Exception while executing task %s: %s\n%s",
                task.id,
                e,
                tb_str,
            )

            # Pass the traceback back to the user as part of the message so they can see details
            error_message = f"Error: {type(e).__name__}: {e!s}\n\nTraceback:\n{tb_str}"

            await updater.update_status(
                TaskState.failed,
                new_agent_text_message(error_message, task.contextId, task.id),
                final=True,
            )
