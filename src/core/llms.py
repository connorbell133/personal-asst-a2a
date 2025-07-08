"""Llms module."""

import os
from typing import Union, Type

from openai import OpenAI
from google import genai
from pydantic import BaseModel


openai_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)


def completion(
    model: str,
    messages: Union[list[dict], str],
    system_prompt: str = "",
) -> str:
    """
    Generate a text completion using the OpenAI API via the OpenRouter endpoint.

    Parameters:
        model (str): Identifier of the model to use for completion.
        messages (Union[list[dict], str]): Input messages as a list of message dictionaries or a single user message string.
        system_prompt (str, optional): An optional system prompt prepended to the messages.

    Returns:
        str: The generated completion text from the API.

    Raises:
        ValueError: If the model parameter is missing or the API response is invalid.
        RuntimeError: If an error occurs during the API call or response processing.
    """
    if not model:
        raise ValueError("Model parameter is required")
    final_messages = []
    if system_prompt:
        final_messages.append({"role": "system", "content": system_prompt})
    if isinstance(messages, str):
        final_messages.extend([{"role": "user", "content": messages}])
    else:
        final_messages.extend(messages)
    try:
        response = openai_client.chat.completions.create(
            model=model,
            messages=final_messages,
        )
        if not response.choices or not response.choices[0].message.content:
            raise ValueError("Invalid response from OpenAI API")
        return response.choices[0].message.content
    except Exception as e:
        raise RuntimeError(f"Failed to generate completion: {str(e)}") from e


genai_client = genai.Client()


def structured_completion(
    model: str,
    contents: str,
    response_schema: Type[BaseModel],
) -> Type[BaseModel]:
    """
    Generate a structured completion using the Google AI API.
    """
    response = genai_client.models.generate_content(
        model=model,
        contents=contents,
        config={
            "response_mime_type": "application/json",
            "response_schema": response_schema,
        },
    )
    parsed_response: response_schema = response.parsed
    return parsed_response
