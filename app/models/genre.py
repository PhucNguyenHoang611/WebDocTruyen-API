from pydantic import BaseModel, Field
from typing import Optional
from utils.model_utils import generate_id

class Genre(BaseModel):
    genre_id: str = Field(default_factory=generate_id)
    name: str
    slug: str
    description: Optional[str] = None