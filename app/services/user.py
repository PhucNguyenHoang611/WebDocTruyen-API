from config.database import dynamodb
from config.email.send_email import send_confirmation_email

from fastapi import BackgroundTasks
from fastapi.responses import JSONResponse
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
from models.user import User

from middleware.auth import generate_token
from middleware.password import verify_password, get_password_hash

from utils.model_utils import generate_totp, verify_totp, generate_verification_key

table = dynamodb.Table("Users")

def login(email: str, password: str):
    try:
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
                        "fullname": item["fullname"]
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
                fullname=user.fullname).dict()

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
    
def verify_email_address(email: str, totp: str):
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
                return JSONResponse(content="Email has been verified", status_code=200)
            else:
                return JSONResponse(content="Invalid verification code", status_code=401)
        else:
            return JSONResponse(content="User not found", status_code=404)
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)