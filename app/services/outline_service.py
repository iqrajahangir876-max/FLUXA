"""FT-12 / T25 - Generate a presentation outline using the AI."""

from app.prompts.outline import OUTLINE_SYSTEM_PROMPT, build_outline_prompt
from app.services.prompt_service import send_prompt_for_json
from app.services.slide_parser import parse_outline


def generate_outline(
    topic: str,
    slide_count: int = 8,
    audience: str = "General audience",
    language: str = "English",
) -> dict:
    """Return {"title": str, "slides": [{slide_number, title, purpose}]}."""

    prompt = build_outline_prompt(
        topic=topic,
        slide_count=slide_count,
        audience=audience,
        language=language,
    )

    data = send_prompt_for_json(prompt, OUTLINE_SYSTEM_PROMPT)

    return parse_outline(data, slide_count)
