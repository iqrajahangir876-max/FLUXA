from dataclasses import dataclass
from typing import Optional


@dataclass
class Presentation:

    id: Optional[int]

    title: str

    description: Optional[str]

    created_at: Optional[str] = None

    updated_at: Optional[str] = None

    def to_dict(self):

        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


@dataclass
class Slide:

    id: Optional[int]

    presentation_id: int

    slide_order: int

    title: Optional[str]

    content: Optional[str]

    created_at: Optional[str] = None

    updated_at: Optional[str] = None

    def to_dict(self):

        return {
            "id": self.id,
            "presentation_id": self.presentation_id,
            "slide_order": self.slide_order,
            "title": self.title,
            "content": self.content,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }