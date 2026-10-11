"""FT-12 / T25 - Prompt templates for generating a presentation outline."""

OUTLINE_SYSTEM_PROMPT = """
You are FLUXA, an AI presentation planning assistant.

Your job is to create a logical outline for a presentation.

Guidelines:
- Use simple, professional language.
- Order the slides logically: introduction, main points,
  examples or evidence, and conclusion.
- Each slide needs a short title and a one-sentence purpose.
- Do not invent facts, statistics, or sources.
- Return valid JSON only, without Markdown code fences.
"""

OUTLINE_USER_PROMPT = """
Create an outline for the following presentation request.

Topic: {topic}
Number of slides: {slide_count}
Audience: {audience}
Language: {language}

Return exactly {slide_count} slides in this JSON structure:
{{
  "title": "Presentation title",
  "slides": [
    {{
      "slide_number": 1,
      "title": "Slide title",
      "purpose": "One sentence describing what this slide achieves"
    }}
  ]
}}
"""


def build_outline_prompt(
    topic: str,
    slide_count: int = 8,
    audience: str = "General audience",
    language: str = "English",
) -> str:
    """Build the outline prompt from the user's presentation request."""

    if not topic or not topic.strip():
        raise ValueError("Presentation topic cannot be empty.")

    if not 1 <= slide_count <= 30:
        raise ValueError("Slide count must be between 1 and 30.")

    return OUTLINE_USER_PROMPT.format(
        topic=topic.strip(),
        slide_count=slide_count,
        audience=audience,
        language=language,
    )
