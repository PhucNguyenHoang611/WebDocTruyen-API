from pydantic import BaseModel, Field
from utils.model_utils import generate_id

class User(BaseModel):
    user_id: str = Field(default_factory=generate_id)
    email: str
    password: str
    fullname: str
    is_verified: bool = False