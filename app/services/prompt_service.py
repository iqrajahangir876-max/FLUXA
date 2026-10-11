"""FT-12 / T24 - Send the user's presentation prompt to the AI."""

from app.services.ai_client import generate_ai_response
from app.services.slide_parser import AIResponseError, extract_json


def send_prompt(prompt: str, system_prompt: str = "") -> str:
    """Send a prompt to the AI and return the raw text response."""

    if not prompt or not prompt.strip():
        raise ValueError("Prompt cannot be empty.")

    return generate_ai_response(prompt=prompt, system_prompt=system_prompt)


def send_prompt_for_json(
    prompt: str,
    system_prompt: str = "",
    max_attempts: int = 2,
) -> dict:
    """Send a prompt and return the response parsed as a JSON object.

    Retries when the AI returns malformed JSON.
    """

    last_error = None

    for _ in range(max_attempts):
        raw = send_prompt(prompt, system_prompt)

        try:
            return extract_json(raw)
        except AIResponseError as error:
            last_error = error

    raise last_error
