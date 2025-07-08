"""Tools for the Gmail Agent."""

import os.path
import base64
import re
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build, Resource
from googleapiclient.errors import HttpError
from pydantic import BaseModel
from src.core.llms import completion, structured_completion

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def get_email_body(payload):
    """Extract and decode email body from Gmail API payload"""
    body = ""

    def extract_body_from_part(part):
        """Helper function to extract body from a message part"""
        if "data" in part.get("body", {}):
            return base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8")
        return ""

    def search_parts_recursively(parts):
        """Recursively search through email parts to find body"""
        for part in parts:
            # Handle nested parts (multipart within multipart)
            if "parts" in part:
                nested_body = search_parts_recursively(part["parts"])
                if nested_body:
                    return nested_body

            # Look for text/plain first (preferred)
            if part.get("mimeType") == "text/plain":
                return extract_body_from_part(part)

        # If no plain text found, look for HTML
        for part in parts:
            if "parts" in part:
                nested_body = search_parts_recursively(part["parts"])
                if nested_body:
                    return nested_body

            if part.get("mimeType") == "text/html":
                return extract_body_from_part(part)

        return ""

    if "parts" in payload:
        # Multipart message - search recursively
        body = search_parts_recursively(payload["parts"])
    else:
        # Simple message
        mime_type = payload.get("mimeType", "")
        if mime_type in ["text/plain", "text/html"]:
            body = extract_body_from_part(payload)

    # Debug info if body is empty
    if not body:
        print(
            f"DEBUG: No body found. Email structure: mimeType={payload.get('mimeType')}, has_parts={'parts' in payload}"
        )
        if "parts" in payload:
            for i, part in enumerate(payload["parts"]):
                print(
                    f"  Part {i}: mimeType={part.get('mimeType')}, has_body_data={'data' in part.get('body', {})}"
                )

    return body


def get_header_value(headers, name):
    """Get header value by name from headers list"""
    for header in headers:
        if header["name"].lower() == name.lower():
            return header["value"]
    return ""


def clean_email_body(body):
    """Clean up email body formatting issues"""
    if not body:
        return body

    lines = body.split("\n")
    cleaned_lines = []

    # Patterns to identify content to remove
    quote_pattern = re.compile(r"^\s*>")  # Lines starting with >
    reply_header_pattern = re.compile(
        r"^On .+? at .+?, .+? wrote:$"
    )  # "On [date] at [time], [person] wrote:"
    signature_patterns = [
        re.compile(r"^Sent via .+$", re.IGNORECASE),
        re.compile(r"^--$"),  # Email signature separator
        re.compile(r"^\s*\(\s*\d{3}\)\s*\d{3}-\d{4}"),  # Phone numbers in parentheses
    ]

    # Track if we're in a quoted section
    in_quote_block = False
    consecutive_empty_lines = 0

    for line in lines:
        stripped_line = line.strip()

        # Skip reply headers
        if reply_header_pattern.match(stripped_line):
            continue

        # Check if line starts a quote block
        if quote_pattern.match(line):
            in_quote_block = True
            continue

        # If we hit a non-quoted line, we're out of quote block
        if in_quote_block and not quote_pattern.match(line) and stripped_line:
            in_quote_block = False

        # Skip quoted lines
        if in_quote_block:
            continue

        # Skip signature patterns
        if any(pattern.match(stripped_line) for pattern in signature_patterns):
            continue

        # Handle empty lines - keep max 1 consecutive empty line
        if not stripped_line:
            consecutive_empty_lines += 1
            if consecutive_empty_lines <= 1:
                cleaned_lines.append("")
            continue

        consecutive_empty_lines = 0

        # Clean up URLs broken into separate parentheses
        # Remove standalone parentheses with URLs
        if re.match(r"^\(\s*https?://[^\s]+\s*\)$", stripped_line):
            continue

        # Clean up the line
        cleaned_line = line

        # Remove extra parentheses around URLs in text
        cleaned_line = re.sub(r"\(\s*(https?://[^\s]+)\s*\)", r"\1", cleaned_line)

        # Remove trailing "tel:" links
        cleaned_line = re.sub(r"\s*\(\s*tel:[^)]+\s*\)", "", cleaned_line)

        cleaned_lines.append(cleaned_line)

    # Join lines and clean up excessive whitespace
    result = "\n".join(cleaned_lines)

    # Remove excessive newlines at start/end
    result = result.strip()

    # Replace multiple consecutive newlines with max 2
    result = re.sub(r"\n{3,}", "\n\n", result)

    return result


def get_emails_sent_to_addresses(addresses: list[str], max_results: int = 100):
    """
    Get emails sent to a list of addresses using server-side filtering for better performance
    """
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w", encoding="utf-8") as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service: Resource = build("gmail", "v1", credentials=creds)

        final_messages = []

        # Use server-side filtering for each address - much more efficient!
        for address in addresses:
            query = f"to:{address}"
            results = (
                service.users()  # pylint: disable=no-member
                .messages()
                .list(userId="me", q=query, maxResults=max_results)  # pylint: disable=no-member
                .execute()
            )
            messages = results.get("messages", [])

            # Now only fetch the messages we actually need
            for message in messages:
                message_data = (
                    service.users()  # pylint: disable=no-member
                    .messages()
                    .get(userId="me", id=message["id"])  # pylint: disable=no-member
                    .execute()
                )
                final_messages.append(message_data)

        return final_messages

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f"An error occurred: {error}")
        return []


def get_emails_sent_from_addresses(addresses: list[str], max_results: int = 100):
    """
    Get emails sent from a list of addresses using server-side filtering for better performance
    """
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w", encoding="utf-8") as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build("gmail", "v1", credentials=creds)

        final_messages = []

        # Use server-side filtering for each address - much more efficient!
        for address in addresses:
            query = f"from:{address}"
            results = (
                service.users()  # pylint: disable=no-member
                .messages()
                .list(userId="me", q=query, maxResults=max_results)  # pylint: disable=no-member
                .execute()
            )
            messages = results.get("messages", [])

            # Now only fetch the messages we actually need
            for message in messages:
                message_data = (
                    service.users()  # pylint: disable=no-member
                    .messages()
                    .get(userId="me", id=message["id"])  # pylint: disable=no-member
                    .execute()
                )
                final_messages.append(message_data)

        return final_messages

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f"An error occurred: {error}")
        return []


def get_tone_from_past_emails(email_address: str) -> str:
    """
    Get the tone of the past emails.
    """
    past_sent_emails = get_emails_sent_to_addresses([email_address])
    past_received_emails = get_emails_sent_from_addresses([email_address])

    past_emails = past_sent_emails + past_received_emails

    if len(past_emails) == 0:
        return """When generating the email, please ensure it embodies the following characteristics:

Tone: Professional and efficient, with a friendly and enthusiastic undertone.

Conciseness: Be direct and to the point, providing only necessary information.

Clarity: Use clear, straightforward language.

Action-Oriented: Clearly state the purpose of the email and any required next steps.

Embedded Links: Include relevant URLs (e.g., LinkedIn profiles, Calendly links, company websites) directly within the body of the email where appropriate, similar to how Ches embeds them.

Polite Directives: Convey requests and instructions politely yet firmly (e.g., "Please find time..." or "That would be appreciated.").

Standard Punctuation: Use standard punctuation; avoid emoticons.

Signature: Conclude with a professional closing like "Thanks," followed by a name, and if applicable, a professional title and contact information (similar to Ches's full signature block).
"""

    emails = []
    for message in past_emails:
        headers = message.get("payload", {}).get("headers", [])
        payload = message.get("payload", {})

        from_email = get_header_value(headers, "From")
        subject = get_header_value(headers, "Subject")
        body = get_email_body(payload)
        clean_body = clean_email_body(body)

        emails.append(
            {
                "from": from_email,
                "subject": subject,
                "body": clean_body,
            }
        )

    # use llm to get the tone and style of the emails in order to determine the tone of the email I am about to send
    prompt = f"""
    You are an expert email analyst. Your task is to analyze the provided past email correspondence associated with the email address '{email_address}' and identify the prevailing tone and communication style.

    **Focus your analysis on the following aspects:**

    * **Overall Tone:** Is it formal, informal, professional, casual, friendly, assertive, neutral, urgent, supportive, demanding, etc.? Provide a primary tone and any secondary tones.
    * **Common Phrases/Vocabulary:** Are there any recurring words, phrases, or jargon?
    * **Sentence Structure:** Are sentences typically long and complex, or short and direct?
    * **Punctuation and Emoticons:** How are these used (e.g., frequent exclamation points, use of emojis, minimal punctuation)?
    * **Level of Detail:** Are the emails concise or detailed?
    * **Call to Action:** How are requests or instructions typically conveyed?

    **Based on your analysis, provide a concise summary of the characteristic tone and communication style. This summary should guide the composition of a new email to ensure consistency with past interactions.**

    **Past Email Correspondence:**
    {emails}
    """
    print(prompt)
    response = completion(
        model="openai/gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )

    return response


def get_email_by_id(email_id: str) -> dict:
    """
    Get an email by id.
    This is a tool that will be used to get an email by id.
    It will return the email as a string.
    """
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    try:
        service = build("gmail", "v1", credentials=creds)
        full_message = (
            service.users()  # pylint: disable=no-member
            .messages()
            .get(userId="me", id=email_id)  # pylint: disable=no-member
            .execute()
        )
        payload = full_message.get("payload", {})
        details = {
            "from": get_header_value(payload.get("headers", []), "From"),
            "subject": get_header_value(payload.get("headers", []), "Subject"),
            "body": get_email_body(payload),
        }
        return details
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None


class EmailResponse(BaseModel):
    """
    A response to an email.
    """

    email: str
    subject: str
    body: str


def get_toned_email_response(email_id: str) -> EmailResponse:
    """
    Get a toned email response for a given email id.
    This is a tool that will be used to get a toned email response for a given email id.
    It will use the tone and style of the past emails to write a new email responding to the given email.
    It will return the new email as a string.
    """
    email = get_email_by_id(email_id)
    if not email:
        return "Error: Email not found"
    tone = get_tone_from_past_emails(email["from"])

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

    response: EmailResponse = structured_completion(
        model="gemini-2.5-flash",
        contents=prompt,
        response_schema=EmailResponse,
    )

    return response
