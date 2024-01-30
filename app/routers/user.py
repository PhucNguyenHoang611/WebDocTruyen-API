from fastapi import APIRouter
from models.user import User
from services.user import login, register
from middleware.auth import validate_token
from pydantic import BaseModel

router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
def login_user(req: LoginRequest):
    return login(req.email, req.password)

@router.post("/register")
def register_user(user: User):
    return register(user)