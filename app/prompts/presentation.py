
PRESENTATION_SYSTEM_PROMPT = """
You are FLUXA, an AI presentation planning assistant.

Your job is to create a clear, well-organized presentation plan
based on the user's topic and requirements.

Guidelines:
- Use simple, professional language.
- Give each slide a clear title and purpose.
- Keep slide content concise and useful.
- Arrange slides in a logical order: introduction, main points,
  examples or evidence, and conclusion.
- Do not invent facts, statistics, or sources.
- Return valid JSON only, without Markdown code fences.
"""

PRESENTATION_USER_PROMPT = """
Create a presentation plan for the following request.

Topic: {topic}
Number of slides: {slide_count}
Audience: {audience}
Language: {language}

Return JSON in this structure:
{{
  "title": "Presentation title",
  "slides": [
    {{
      "slide_number": 1,
      "title": "Slide title",
      "key_points": [
        "First key point",
        "Second key point"
      ],
      "visual_suggestion": "Suggested image, chart, or diagram"
    }}
  ]
}}
"""


def build_presentation_prompt(
    topic: str,
    slide_count: int = 8,
    audience: str = "General audience",
    language: str = "English",
) -> str:
    """Build a user prompt from the presentation requirements."""

    if not topic.strip():
        raise ValueError("Presentation topic cannot be empty.")

    if not 1 <= slide_count <= 30:
        raise ValueError("Slide count must be between 1 and 30.")

    return PRESENTATION_USER_PROMPT.format(
        topic=topic.strip(),
        slide_count=slide_count,
        audience=audience,
        language=language,
    )