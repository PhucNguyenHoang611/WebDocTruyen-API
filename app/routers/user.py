from fastapi import APIRouter, BackgroundTasks
from models.user import User
from services.user import login, register, send_verification_code, verify_email_address
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
def register_user(background_tasks: BackgroundTasks, user: User):
    return register(background_tasks, user)

@router.post("/sendVerificationEmail/{email}")
def send_verification_email(background_tasks: BackgroundTasks, email: str):
    return send_verification_code(background_tasks, email)

@router.get("/verifyEmail/", include_in_schema=False)
def verify_email(email: str, totp: str):
    return verify_email_address(email, totp)