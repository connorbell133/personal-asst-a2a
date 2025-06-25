"""Tool Client module."""

import json
import uuid
from typing import Any

import httpx
import requests

# ---------- Logfire instrumentation ----------
# Try to import Logfire if available. We wrap this in a try/except so that the
# rest of the library still works when Logfire is not installed or an older
# version is present (e.g. during CI or minimal deployments).

try:
    import logfire

    if hasattr(logfire, "configure"):
        # We only need to call configure once per process. If the user has
        # already configured Logfire (e.g. in ``app.py``) this call will be a
        # no-op. We still add it here so that the module can be imported and
        # used stand-alone in other scripts without additional setup.
        logfire.configure(send_to_logfire=False)

        # Instrument common libraries used by the tool client so that HTTP
        # traffic appears automatically in Logfire's Live view.
        for _instr in (
            getattr(logfire, "instrument_httpx", None),
            getattr(logfire, "instrument_requests", None),
        ):
            if callable(_instr):
                try:
                    _instr()
                except Exception:
                    # Instrumentation failure shouldn't crash the app.
                    pass

    # Expose decorator helper only if Logfire import succeeded
    span = getattr(logfire, "instrument", lambda *a, **k: (lambda f: f))

except ModuleNotFoundError:
    # Logfire not installed; define a no-op decorator so the rest of the code
    # still imports and works.
    def span(*_args, **_kwargs):  # type: ignore
        """
        A no-op decorator that acts as a placeholder for span tracing when Logfire is unavailable.
        
        This decorator can be applied to functions to maintain compatibility with tracing instrumentation, but it does not modify the behavior of the decorated function.
        """

        def _decorator(func):
            """
            A no-op decorator that returns the original function unchanged.
            """
            return func

        return _decorator


# -------------------------------------------------------------

from a2a.client import A2AClient
from a2a.types import AgentCard, MessageSendParams, SendMessageRequest


class A2AToolClient:
    """A2A client."""

    def __init__(self, default_timeout: float = 120.0):
        # Cache for agent metadata - also serves as the list of registered agents
        # None value indicates agent is registered but metadata not yet fetched
        self._agent_info_cache: dict[str, dict[str, Any] | None] = {}
        # Default timeout for requests (in seconds)
        self.default_timeout = default_timeout

    def _normalize_url(self, url: str) -> str:
        """Ensure the URL contains a scheme and has no trailing slash."""
        if not url.startswith(("http://", "https://")):
            url = f"http://{url}"
        return url.rstrip("/")

    # -------------------- Public API --------------------

    @span("A2AToolClient.add_remote_agent", extract_args=True)
    def add_remote_agent(self, agent_url: str):
        """Add agent to the list of available remote agents."""
        normalized_url = self._normalize_url(agent_url)
        if normalized_url not in self._agent_info_cache:
            # Initialize with None to indicate metadata not yet fetched
            self._agent_info_cache[normalized_url] = None

    @span("A2AToolClient.list_remote_agents")
    def list_remote_agents(self) -> list[dict[str, Any]]:
        """List available remote agents with caching."""
        if not self._agent_info_cache:
            return []

        remote_agents_info = []
        for remote_connection in self._agent_info_cache:
            # Use cached data if available
            if self._agent_info_cache[remote_connection] is not None:
                remote_agents_info.append(self._agent_info_cache[remote_connection])
            else:
                try:
                    # Fetch and cache agent info
                    agent_info = requests.get(
                        f"{remote_connection}/.well-known/agent.json"
                    )
                    agent_data = agent_info.json()
                    self._agent_info_cache[remote_connection] = agent_data
                    remote_agents_info.append(agent_data)
                except Exception as e:
                    print(f"Failed to fetch agent info from {remote_connection}: {e}")

        return self._agent_info_cache

    @span("A2AToolClient.create_task", extract_args=True)
    async def create_task(self, agent_url: str, message: str) -> str:
        """Send a message following the official A2A SDK pattern."""
        # Normalise the agent URL first so that downstream libraries always
        # receive a valid absolute URL. This prevents errors such as
        # "Request URL is missing an 'http://' or 'https://' protocol." when
        # a caller accidentally omits the scheme.
        agent_url = self._normalize_url(agent_url)

        # Configure httpx client with timeout
        timeout_config = httpx.Timeout(
            timeout=self.default_timeout,
            connect=10.0,
            read=self.default_timeout,
            write=10.0,
            pool=5.0,
        )

        async with httpx.AsyncClient(timeout=timeout_config) as httpx_client:
            # Check if we have cached agent card data
            if (
                agent_url in self._agent_info_cache
                and self._agent_info_cache[agent_url] is not None
            ):
                agent_card_data = self._agent_info_cache[agent_url]
            else:
                # Fetch the agent card
                agent_card_response = await httpx_client.get(
                    f"{agent_url}/.well-known/agent.json"
                )
                agent_card_data = agent_card_response.json()

            # Create AgentCard from data
            agent_card = AgentCard(**agent_card_data)

            # Create A2A client with the agent card
            client = A2AClient(httpx_client=httpx_client, agent_card=agent_card)

            # Build the message parameters following official structure
            send_message_payload = {
                "message": {
                    "role": "user",
                    "parts": [{"kind": "text", "text": message}],
                    "messageId": uuid.uuid4().hex,
                }
            }

            # Create the request
            request = SendMessageRequest(
                id=str(uuid.uuid4()), params=MessageSendParams(**send_message_payload)
            )

            # Send the message with timeout configuration
            response = await client.send_message(request)

            # Extract text from response
            try:
                response_dict = response.model_dump(mode="json", exclude_none=True)
                if "result" in response_dict and "artifacts" in response_dict["result"]:
                    artifacts = response_dict["result"]["artifacts"]
                    for artifact in artifacts:
                        if "parts" in artifact:
                            for part in artifact["parts"]:
                                if "text" in part:
                                    return part["text"]

                # If we couldn't extract text, return the full response as formatted JSON
                return json.dumps(response_dict, indent=2)

            except Exception as e:
                # Log the error and return string representation
                print(f"Error parsing response: {e}")
                return str(response)

    def remove_remote_agent(self, agent_url: str):
        """Remove an agent from the list of available remote agents."""
        normalized_url = self._normalize_url(agent_url)
        if normalized_url in self._agent_info_cache:
            del self._agent_info_cache[normalized_url]
