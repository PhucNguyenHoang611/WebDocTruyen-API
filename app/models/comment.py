from pydantic import BaseModel, Field
from utils.model_utils import generate_id, generate_date

class Comment(BaseModel):
    comment_id: str = Field(default_factory=generate_id)
    user_id: str
    story_id: str
    content: str
    time: str = Field(default_factory=generate_date)