from pydantic import BaseModel, Field
from typing import Optional, List
from utils.model_utils import generate_id

class Story(BaseModel):
    story_id: str = Field(default_factory=generate_id)
    title: str
    synopsis: Optional[str] = None
    cover_image_url: str
    author: str
    genres: str # List[str]
    tags: str
    chapters_count: int = 0
    status: str
    views: int = 0
    rating: int = 0
    total_votes: int = 0