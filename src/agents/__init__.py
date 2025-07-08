"""Agents module module."""

from .calendar_agent import calendar_agent, CalendarAgentCard
from .gmail_agent import gmail_agent, GmailAgentCard
from .obsidian_agent import obsidian_agent, ObsidianAgentCard
from .todoist_agent import todoist_agent, TodoistAgentCard
from .orchestration_agent import (
    OrchestrationAgentCard,
    orchestration_agent,
    a2a_client,
)
from .common.agent_manager import agent_manager
from .common.agent import run_agent_in_background

__all__ = [
    "calendar_agent",
    "CalendarAgentCard",
    "gmail_agent",
    "GmailAgentCard",
    "obsidian_agent",
    "ObsidianAgentCard",
    "todoist_agent",
    "TodoistAgentCard",
    "orchestration_agent",
    "OrchestrationAgentCard",
    "a2a_client",
    "agent_manager",
    "run_agent_in_background",
]
