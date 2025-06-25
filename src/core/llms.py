"""Llms module."""

import os
from typing import Union

from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)


def completion(
    model: str,
    messages: Union[list[dict], str],
    system_prompt: str = "",
) -> str:
    """
    Generate a completion using the OpenAI API.
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
        response = client.chat.completions.create(
            model=model,
            messages=final_messages,
        )
        if not response.choices or not response.choices[0].message.content:
            raise ValueError("Invalid response from OpenAI API")
        return response.choices[0].message.content
    except Exception as e:
        raise RuntimeError(f"Failed to generate completion: {str(e)}") from e
