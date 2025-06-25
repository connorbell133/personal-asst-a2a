"""Agents module module."""

from .calendar_agent import calendar_agent, CalendarAgentCard
from .gmail_agent import gmail_agent, GmailAgentCard
from .obsidian_agent import obsidian_agent, ObsidianAgentCard
from .todoist_agent import todoist_agent, TodoistAgentCard
from .orchestration_agent import create_orchestration_agent, OrchestrationAgentCard

__all__ = [
    "calendar_agent",
    "CalendarAgentCard",
    "gmail_agent",
    "GmailAgentCard",
    "obsidian_agent",
    "ObsidianAgentCard",
    "todoist_agent",
    "TodoistAgentCard",
    "create_orchestration_agent",
    "OrchestrationAgentCard",
]
