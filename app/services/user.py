from config.database import dynamodb
from fastapi.responses import JSONResponse
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
from models.user import User

from middleware.auth import generate_token
from middleware.password import verify_password, get_password_hash

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
        return JSONResponse(content=e.response["error"], status_code=500)

def register(user: dict):
    try:
        response = table.query(
            IndexName="EmailIndex",
            KeyConditionExpression=Key("email").eq(user["email"])
        )
        items = response["Items"]

        if items:
            return JSONResponse(content="Email already exists", status_code=409)
        else:
            user["password"] = get_password_hash(user["password"])
            item = User(
                email=user["email"],
                password=user["password"],
                fullname=user["fullname"]).dict()

            table.put_item(Item=item)
            return JSONResponse(content=item, status_code=201)
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)

# def get_user_by_email(email: str):
#     try:
#         response = table.query(
#             IndexName="EmailIndex",
#             KeyConditionExpression=Key("email").eq(email)
#         )
#         items = response["Items"]

#         if items:
#             return JSONResponse(
#                 content={
#                     "email": items[0]["email"],
#                     "fullname": items[0]["fullname"]
#                 },
#                 status_code=200
#             )
#         else:
#             return JSONResponse(content="User not found", status_code=404)
#     except ClientError as e:
#         return JSONResponse(content=e.response["Error"], status_code=500)