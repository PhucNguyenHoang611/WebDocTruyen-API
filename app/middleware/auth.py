import os
from config.database import dynamodb
from pathlib import Path
from dotenv import load_dotenv
import jwt
from typing import Union, Any
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

from boto3.dynamodb.conditions import Key
from pydantic import ValidationError


base_dir = Path(__file__).parent.parent.parent
load_dotenv(base_dir.joinpath(".env"))

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")

reuseable_oauth2 = HTTPBearer(
    scheme_name="Authorization"
)

def get_user(email: str):
    response = dynamodb.Table("Users").query(
        IndexName="EmailIndex",
        KeyConditionExpression=Key("email").eq(email)
    )
    items = response["Items"]

    if items:
        return items[0]
    else:
        return None

def validate_token(http_authorization_credentials=Depends(reuseable_oauth2)) -> str:
    try:
        payload = jwt.decode(http_authorization_credentials.credentials, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])

        if payload.get("exp") < datetime.utcnow().timestamp():
            raise HTTPException(status_code=403, detail="Token has expired")

        user = get_user(payload.get("email"))

        if user is None:
            raise HTTPException(status_code=403, detail="Invalid user")
        else:
            return user
    except (jwt.PyJWTError, ValidationError):
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    
def generate_token(email: Union[str, Any]) -> str:
    expire = datetime.utcnow() + timedelta(
        seconds = 60 * 60 * 24 * 3 # Expired after 3 days
    )
    to_encode = {
        "exp": expire,
        "email": email
    }
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt