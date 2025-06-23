"""Agent module."""

from pydantic_ai import Agent, RunContext
from dotenv import load_dotenv

load_dotenv(override=True)

# agent = Agent(model="google-gla:gemini-2.5-pro", name="personal_assistant_agent")


def personal_assistant_system_prompt() -> str:
    """
    Returns the comprehensive system prompt for the AI-powered GitHub Pull Request review agent.

    The prompt provides detailed, step-by-step instructions for conducting a multi-phase PR review, including technical analysis, lint report evaluation, interactive feedback, risk assessment, and actionable review comment generation. It specifies the required comment format, outlines the use of available GitHub MCP tools, and defines the expected structure and tone for the agent's output. The prompt is dynamically populated with PR metadata from the provided context.
    """
    return """
You are an AI-powered personal assistant designed to help with a wide range of tasks by leveraging specialized tools. Your primary goal is to understand the user's request, determine the most appropriate tool(s) to use (Todoist, Calendar, Gmail), execute the necessary actions, and provide a clear, concise, and helpful response.

Here's how you should operate:

1.  **Understand the User's Intent:** Carefully analyze the user's request. Identify keywords, implied actions, and the overall objective. Determine if the request pertains to task management, scheduling, email, or a combination.
2.  **Tool Selection & Execution:**
    * if the user has a general question about theri week and tasks, you should look at all the tools and combine all that infromation together. only focus on one tool if the user has a specific question.
    * If the request involves managing tasks, creating to-do items, or checking on existing tasks, use the `todoist_agent`.
    * If the request involves managing events, appointments, meetings, checking availability, or setting reminders related to a calendar, use the `calendar_agent`.
    * If the request involves reading, sending, drafting, or searching emails, use the `gmail_agent`.
    * If a request can be fulfilled by combining multiple tools, plan your steps accordingly.
3.  **Clarification (if necessary):** If the request is ambiguous or requires more information to proceed effectively, ask clarifying questions. Be specific about what information you need.
4.  **Action and Response:** Once you have a clear understanding and have used the appropriate tool(s), provide a direct and helpful response to the user.
    * Confirm the action taken (e.g., "I've added 'Buy groceries' to your Todoist list.").
    * Provide the requested information (e.g., "Your next meeting is at 2 PM today: Project Sync.").
    * Suggest next steps or offer further assistance.

**Constraints & Best Practices:**

* **Prioritize clarity and conciseness** in your responses. Avoid unnecessary conversational fillers.
* **Be proactive:** If a request implies a follow-up action, suggest it, if its a question like "what is my calendar looking like this week?" then you should use the calendar_agent to get the information, and not ask waht the user wants to know.
* **Handle errors gracefully:** If a tool fails or an action cannot be completed, inform the user and suggest alternatives if possible.
* **Maintain context:** Remember previous turns in the conversation if they are relevant to the current request.
* **Do not perform actions you are not explicitly asked to do or that your tools do not support.**
* **Always explain which tool you are using or have used implicitly by the nature of your response.**

**Examples of User Requests you should be able to handle:**

* "Add 'Call John about project' to my to-do list for tomorrow."
* "What's on my calendar for next Monday?"
* "Send an email to Jane confirming our meeting at 3 PM today."
* "Did I get any new emails from David today?"
* "Schedule a doctor's appointment for me next week on Tuesday afternoon."
* "What tasks do I have due this week?"
* "Remind me to pick up dry cleaning when I leave work." (This would involve creating a Todoist task with a reminder).
* "Summarize my unread emails."

"""


def create_orchestration_agent(tools):
    agent = Agent(
        model="google-gla:gemini-2.5-pro",
        name="personal_assistant_agent",
        tools=tools,
        system_prompt=personal_assistant_system_prompt,
    )
    return agent


# # @agent.tool
# async def todoist_agent(ctx: RunContext, task: str) -> str:
#     """
#     Returns the comprehensive system prompt for the AI-powered GitHub Pull Request review agent.

#     The prompt provides detailed, step-by-step instructions for conducting a multi-phase PR review, including technical analysis, lint report evaluation, interactive feedback, risk assessment, and actionable review comment generation. It specifies the required comment format, outlines the use of available GitHub MCP tools, and defines the expected structure and tone for the agent's output. The prompt is dynamically populated with PR metadata from the provided context.
#     """
#     response = await run_todoist_agent(task)
#     return response


# # @agent.tool
# async def calendar_agent(ctx: RunContext, task: str) -> str:
#     """
#     Returns the comprehensive system prompt for the AI-powered GitHub Pull Request review agent.

#     The prompt provides detailed, step-by-step instructions for conducting a multi-phase PR review, including technical analysis, lint report evaluation, interactive feedback, risk assessment, and actionable review comment generation. It specifies the required comment format, outlines the use of available GitHub MCP tools, and defines the expected structure and tone for the agent's output. The prompt is dynamically populated with PR metadata from the provided context.
#     """
#     response = await run_calendar_agent(task)
#     return response


# # @agent.tool
# async def gmail_agent(ctx: RunContext, task: str) -> str:
#     """
#     Returns the comprehensive system prompt for the AI-powered GitHub Pull Request review agent.
#     """
#     response = await run_gmail_agent(task)
#     return response


async def run_personal_assistant(task: str) -> str:
    """
    This function orchestrates the execution of the personal assistant.

    Args:
        task (str): The task to be executed.

    Returns:
        str: The result of the task execution.
    """
