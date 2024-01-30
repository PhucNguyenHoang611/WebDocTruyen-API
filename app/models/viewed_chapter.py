from pydantic import BaseModel, Field
from utils.model_utils import generate_id, generate_date

class ViewedChapter(BaseModel):
    user_id: str = Field(default_factory=generate_id)
    chapter_id: str
    completed_date: str = Field(default_factory=generate_date)