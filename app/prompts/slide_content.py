"""FT-12 / T26 - Prompt templates for generating slide content."""

import json

SLIDE_CONTENT_SYSTEM_PROMPT = """
You are FLUXA, an AI presentation writing assistant.

Your job is to write the content of each slide in an approved outline.

Guidelines:
- Use simple, professional language.
- Give each slide 3 to 5 concise key points (one short sentence each).
- Keep the slide numbers and titles from the outline.
- Do not invent facts, statistics, or sources.
- Return valid JSON only, without Markdown code fences.
"""

SLIDE_CONTENT_USER_PROMPT = """
Write the slide content for this presentation.

Presentation title: {title}
Topic: {topic}
Audience: {audience}
Language: {language}

Outline:
{outline_json}

Return JSON in this structure, one entry per outline slide:
{{
  "slides": [
    {{
      "slide_number": 1,
      "title": "Slide title",
      "key_points": [
        "First key point",
        "Second key point"
      ]
    }}
  ]
}}
"""


def build_slide_content_prompt(
    topic: str,
    title: str,
    outline: list,
    audience: str = "General audience",
    language: str = "English",
) -> str:
    """Build the slide-content prompt from an already parsed outline."""

    if not topic or not topic.strip():
        raise ValueError("Presentation topic cannot be empty.")

    if not outline:
        raise ValueError("Outline cannot be empty.")

    return SLIDE_CONTENT_USER_PROMPT.format(
        title=title,
        topic=topic.strip(),
        audience=audience,
        language=language,
        outline_json=json.dumps(outline, indent=2, ensure_ascii=False),
    )
