import base64
from uuid import uuid4
from datetime import datetime
from passlib.totp import generate_secret
import pyotp

def generate_id():
    return str(uuid4())

def generate_date():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return str(dt_string)

def generate_verification_key():
    secret = generate_secret()
    encoded_secret = base64.b32encode(secret.encode()).decode()
    return encoded_secret

# TOTP Management

def verify_totp(to_verify: str, my_secret: str) -> bool:
    totp = pyotp.TOTP(my_secret, interval=3600)
    return totp.verify(to_verify)
    
def generate_totp(my_secret: str) -> str:
    totp = pyotp.TOTP(my_secret, interval=3600)
    otp = totp.now()
    return otp