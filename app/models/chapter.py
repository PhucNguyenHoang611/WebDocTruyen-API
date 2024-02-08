from pydantic import BaseModel, Field
from utils.model_utils import generate_id, generate_date

class Chapter(BaseModel):
    chapter_id: str = Field(default_factory=generate_id)
    story_id: str
    chapter_number: int = 0
    title: str
    content_url: str
    created_at: str = Field(default_factory=generate_date)