from pydantic import BaseModel, Field
from typing import Optional, List
from utils.model_utils import generate_id, generate_date

class Story(BaseModel):
    story_id: str = Field(default_factory=generate_id)
    title: str
    synopsis: Optional[str] = None
    cover_image_url: str
    author: str
    genres: List[str]
    tags: List[str]
    chapters_count: int = 0
    status: str
    views: int = 0
    rating: int = 0
    total_votes: int = 0
    created_at: str = Field(default_factory=generate_date)