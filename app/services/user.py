import os
from pathlib import Path
from dotenv import load_dotenv
from config.database import dynamodb
from config.email.send_email import send_confirmation_email, send_forget_password_email

from fastapi import BackgroundTasks, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
from models.user import User

from middleware.auth import generate_token, generate_token_admin
from middleware.password import verify_password, get_password_hash

from utils.model_utils import generate_totp, verify_totp, generate_verification_key

base_dir = Path(__file__).parent.parent.parent
load_dotenv(base_dir.joinpath(".env"))

table = dynamodb.Table("Users")

def login(email: str, password: str):
    try:
        if email == os.getenv("ADMIN_EMAIL") and password == os.getenv("ADMIN_PASSWORD"):
            return JSONResponse(
                content={
                    "token": generate_token_admin(email, password),
                    "email": email,
                    "fullname": "Admin"
                },
                status_code=200
            )

        response = table.query(
            IndexName="EmailIndex",
            KeyConditionExpression=Key("email").eq(email)
        )
        items = response["Items"]

        if items:
            item = items[0]

            if verify_password(password, item["password"]):
                return JSONResponse(
                    content={
                        "token": generate_token(email),
                        "email": item["email"],
                        "fullname": item["fullname"],
                        "gender": item["gender"],
                        "year_of_birth": item["year_of_birth"]
                    },
                    status_code=200
                )
            else:
                return JSONResponse(content="Invalid credentials", status_code=401)     
        else:
            return JSONResponse(content="User not found", status_code=404)
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)

def register(background_tasks: BackgroundTasks, user: User):
    try:
        response = table.query(
            IndexName="EmailIndex",
            KeyConditionExpression=Key("email").eq(user.email)
        )
        items = response["Items"]

        if items:
            return JSONResponse(content="Email already exists", status_code=409)
        else:
            user.password = get_password_hash(user.password)
            item = User(
                email=user.email,
                password=user.password,
                fullname=user.fullname,
                gender=user.gender,
                year_of_birth=user.year_of_birth,
                role="User").dict()

            table.put_item(Item=item)

            totp = generate_totp(item["verification_key"])
            send_confirmation_email(background_tasks, item["email"], item["fullname"], totp)

            return JSONResponse(content="Verification code has been sent to your email", status_code=201)
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)
    
def send_verification_code(background_tasks: BackgroundTasks, email: str):
    try:
        response = table.query(
            IndexName="EmailIndex",
            KeyConditionExpression=Key("email").eq(email)
        )
        items = response["Items"]

        if items:
            item = items[0]
            new_verification_key = generate_verification_key()

            table.update_item(
                Key={"user_id": item["user_id"]},
                UpdateExpression="set verification_key = :vk",
                ExpressionAttributeValues={":vk": new_verification_key}
            )

            totp = generate_totp(new_verification_key)
            send_confirmation_email(background_tasks, item["email"], item["fullname"], totp)

            return JSONResponse(content="Verification code has been sent to your email", status_code=200)
        else:
            return JSONResponse(content="User not found", status_code=404)
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)

templates = Jinja2Templates(directory="templates")
    
def verify_email_address(request: Request, email: str, totp: str):
    try:
        response = table.query(
            IndexName="EmailIndex",
            KeyConditionExpression=Key("email").eq(email)
        )
        items = response["Items"]

        if items:
            item = items[0]

            if verify_totp(totp, item["verification_key"]):
                table.update_item(
                    Key={"user_id": item["user_id"]},
                    UpdateExpression="set is_verified = :iv",
                    ExpressionAttributeValues={":iv": True}
                )
                return templates.TemplateResponse(request=request, name="verify_success.html")
            else:
                return JSONResponse(content="Invalid verification code", status_code=401)
        else:
            return JSONResponse(content="User not found", status_code=404)
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)
    
# Forget password
def forget_pwd(background_tasks: BackgroundTasks, email: str):
    try:
        response = table.query(
            IndexName="EmailIndex",
            KeyConditionExpression=Key("email").eq(email)
        )
        items = response["Items"]

        if items:
            item = items[0]
            new_verification_key = generate_verification_key()

            table.update_item(
                Key={"user_id": item["user_id"]},
                UpdateExpression="set verification_key = :vk",
                ExpressionAttributeValues={":vk": new_verification_key}
            )

            totp = generate_totp(new_verification_key)
            send_forget_password_email(background_tasks, item["email"], item["fullname"], totp)

            return JSONResponse(content="Verification code has been sent to your email", status_code=200)
        else:
            return JSONResponse(content="User not found", status_code=404)
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)
    
def reset_pwd(email: str, totp: str, new_password: str):
    try:
        response = table.query(
            IndexName="EmailIndex",
            KeyConditionExpression=Key("email").eq(email)
        )
        items = response["Items"]

        if items:
            item = items[0]

            if verify_totp(totp, item["verification_key"]):
                new_password = get_password_hash(new_password)
                table.update_item(
                    Key={"user_id": item["user_id"]},
                    UpdateExpression="set password = :p",
                    ExpressionAttributeValues={":p": new_password}
                )

                return JSONResponse(content="Password has been reset", status_code=200)
            else:
                return JSONResponse(content="Invalid verification code", status_code=401)
        else:
            return JSONResponse(content="User not found", status_code=404)
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)

# Change password
def change_pwd(email: str, old_password: str, new_password: str):
    try:
        response = table.query(
            IndexName="EmailIndex",
            KeyConditionExpression=Key("email").eq(email)
        )
        items = response["Items"]

        if items:
            item = items[0]

            if verify_password(old_password, item["password"]):
                new_password = get_password_hash(new_password)
                table.update_item(
                    Key={"user_id": item["user_id"]},
                    UpdateExpression="set password = :p",
                    ExpressionAttributeValues={":p": new_password}
                )

                return JSONResponse(content="Password has been changed", status_code=200)
            else:
                return JSONResponse(content="Invalid old password", status_code=401)
        else:
            return JSONResponse(content="User not found", status_code=404)
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)

# Update user information
def update_user(email: str, user: User):
    try:
        response = table.query(
            IndexName="EmailIndex",
            KeyConditionExpression=Key("email").eq(email)
        )
        items = response["Items"]

        if items:
            item = items[0]

            table.update_item(
                Key={"user_id": item["user_id"]},
                UpdateExpression="set #fullname=:fullname, #gender=:gender, #year_of_birth=:year_of_birth",
                ExpressionAttributeValues={
                    ":fullname": user.fullname,
                    ":gender": user.gender,
                    ":year_of_birth": user.year_of_birth
                },
                ExpressionAttributeNames={
                    "#fullname": "fullname",
                    "#gender": "gender",
                    "#year_of_birth": "year_of_birth"
                }
            )

            return JSONResponse(content="Update user information successfully", status_code=200)
        else:
            return JSONResponse(content="User not found", status_code=404)
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)