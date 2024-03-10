from fastapi import APIRouter, BackgroundTasks, Request, Depends
from models.user import User
from services.user import login, register, send_verification_code, verify_email_address, forget_pwd, reset_pwd, change_pwd, update_user
from middleware.auth import validate_token
from pydantic import BaseModel

router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    email: str
    password: str
    fullname: str
    gender: str
    year_of_birth: int

class ResetPasswordRequest(BaseModel):
    email: str
    totp: str
    new_password: str

class ChangePasswordRequest(BaseModel):
    email: str
    old_password: str
    new_password: str

class UpdateUserInformationRequest(BaseModel):
    fullname: str
    gender: str
    year_of_birth: int

@router.post("/login")
def login_user(req: LoginRequest):
    return login(req.email, req.password)

@router.post("/register")
def register_user(background_tasks: BackgroundTasks, req: RegisterRequest):
    return register(background_tasks, req.email, req.password, req.fullname, req.gender, req.year_of_birth)

@router.post("/sendVerificationEmail/{email}")
def send_verification_email(background_tasks: BackgroundTasks, email: str):
    return send_verification_code(background_tasks, email)

@router.get("/verifyEmail/", include_in_schema=False)
def verify_email(request: Request, email: str, totp: str):
    return verify_email_address(request, email, totp)

@router.post("/forgetPassword/{email}")
def forget_password(background_tasks: BackgroundTasks, email: str):
    return forget_pwd(background_tasks, email)

@router.post("/resetPassword")
def reset_password(request: ResetPasswordRequest):
    return reset_pwd(request.email, request.totp, request.new_password)

@router.post("/changePassword", dependencies=[Depends(validate_token)])
def change_password(request: ChangePasswordRequest):
    return change_pwd(request.email, request.old_password, request.new_password)

@router.put("/updateUserInformation/{email}", dependencies=[Depends(validate_token)])
def update_user_information(email: str, req: UpdateUserInformationRequest):
    return update_user(email, req.fullname, req.gender, req.year_of_birth)