from pydantic import BaseModel, Field
from utils.model_utils import generate_id, generate_date

class Response(BaseModel):
    response_id: str = Field(default_factory=generate_id)
    parent_id: str
    user_id: str
    content: str
    time: str = Field(default_factory=generate_date)