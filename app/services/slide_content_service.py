"""FT-12 / T26 - Generate slide content from an outline using the AI."""

from app.prompts.slide_content import (
    SLIDE_CONTENT_SYSTEM_PROMPT,
    build_slide_content_prompt,
)
from app.services.prompt_service import send_prompt_for_json
from app.services.slide_parser import parse_slide_content


def generate_slide_content(
    topic: str,
    outline: dict,
    audience: str = "General audience",
    language: str = "English",
) -> list:
    """Return [{slide_number, title, key_points}] for every outline slide."""

    prompt = build_slide_content_prompt(
        topic=topic,
        title=outline["title"],
        outline=outline["slides"],
        audience=audience,
        language=language,
    )

    data = send_prompt_for_json(prompt, SLIDE_CONTENT_SYSTEM_PROMPT)

    return parse_slide_content(data, outline["slides"])
