from pydantic import BaseModel, Field
from utils.model_utils import generate_date

class ViewedChapter(BaseModel):
    user_id: str
    chapter_id: str
    completed_date: str = Field(default_factory=generate_date)