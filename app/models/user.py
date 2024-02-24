from pydantic import BaseModel, Field
from utils.model_utils import generate_id, generate_verification_key

class User(BaseModel):
    user_id: str = Field(default_factory=generate_id)
    email: str
    password: str
    fullname: str
    gender: str
    year_of_birth: int
    role: str
    is_verified: bool = False
    verification_key: str = Field(default_factory=generate_verification_key)