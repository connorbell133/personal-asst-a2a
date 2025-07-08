"""Agent module."""

from datetime import datetime
from dotenv import load_dotenv
from pydantic_ai import Agent, RunContext
from a2a.types import AgentSkill
from src.mcp_servers.gmail import server as gmail_server
from src.agents.common.agent import load_agent_config
from src.core.logger import logger
from src.agents.gmail_agent.tools import (
    get_email_by_id,
    get_tone_from_past_emails,
    EmailResponse,
)
from src.core.llms import structured_completion

load_dotenv(override=True)

# Load agent configuration
gmail_agent_config = load_agent_config("src/agents/gmail_agent/config.yml")


# Instantiate the agent card
class GmailAgentCard:
    """
    Gmail Agent Card.
    """

    name: str = gmail_agent_config.name
    description: str = gmail_agent_config.description
    skills: list[AgentSkill] = []
    organization: str = gmail_agent_config.name
    port: int = gmail_agent_config.port
    host: str = gmail_agent_config.host


# Instantiate the agent
gmail_agent = Agent(
    model=gmail_agent_config.model,
    mcp_servers=[gmail_server],
    name=gmail_agent_config.name,
    system_prompt=gmail_agent_config.system_prompt.format(
        current_date=datetime.now().strftime("%Y-%m-%d")
    ),
)

# Convert the agent to an A2A agent
app = gmail_agent.to_a2a()


@gmail_agent.tool
def get_toned_email_response(ctx: RunContext, email_id: str) -> EmailResponse:
    """
    Generates a new email response, matching the tone and style of past communications.

    This tool is designed to draft an email reply to a specific incoming email,
    automatically adapting to the sender's previously established writing style.
    It's ideal for maintaining consistent communication tone.

    Args:
        email_id (str): The unique identifier of the incoming email to which a response is needed.

    Returns:
        Email_Response: An object containing the generated reply email's full content,
                        its subject, and its body, formatted for sending.
    """
    logger.info("Getting toned email response for email_id: %s", email_id)
    email = get_email_by_id(email_id)
    if not email:
        return "Error: Email not found"
    tone = get_tone_from_past_emails(email["from"])
    logger.info("Tone: %s", tone)
    # --- Improved Prompt ---
    prompt = (
        "You are Connor Bell. Your goal is to draft a reply email that perfectly matches the established tone and style from your past correspondence."
        "\n\n"  # Added line breaks for readability in the prompt
        "Here's the email you need to respond to:"
        "\n\n"
        "--- Incoming Email ---\n"  # Clear delimiters
        f"Subject: {email['subject']}\n"
        f"From: {email['from']}\n"
        f"Body:\n{email['body']}\n"
        "--- End Incoming Email ---\n"
        "\n\n"
        "Here's the detailed description of your established tone and style, based on your past emails. Pay close attention to these elements when crafting your response:"
        "\n\n"
        "--- Connor Bell's Tone and Style ---\n"  # Clear delimiters
        f"{tone}\n"  # This 'tone' variable should ideally contain actual examples or a detailed description.
        "--- End Tone and Style ---\n"
        "\n\n"
        "Specifically, consider:\n"
        "* **Formality/Informality:** Are you casual, professional, or somewhere in between? Do you use contractions or slang?\n"
        "* **Sentence Structure & Length:** Are your sentences typically short and direct, or more elaborate?\n"
        "* **Common Phrases:** Do you have any signature greetings, closings, or common phrases you use often?\n"
        "* **Overall Persona:** Are you direct, friendly, concise, detailed, humorous, etc.?\n"
        "\n\n"
        "Based on the incoming email and your defined tone, please draft the reply email. Ensure the response is a valid email, including appropriate line breaks and spacing for readability."
        "\n\n"
        "**Your response MUST be the complete email body only, ready to be sent, and should fit the `Email_Response` schema.**"  # Emphasized output format
    )
    # --- End Improved Prompt ---
    logger.info("Prompt: %s", prompt)
    response: EmailResponse = structured_completion(
        model="gemini-2.5-flash",
        contents=prompt,
        response_schema=EmailResponse,
    )
    logger.info("Response: %s", response)
    return response
