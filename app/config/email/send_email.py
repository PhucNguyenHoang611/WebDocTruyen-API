import os
from pathlib import Path
from typing import List
from fastapi import BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema, MessageType, ConnectionConfig
from pydantic import BaseModel, EmailStr

from dotenv import load_dotenv

templates_dir = Path(__file__).parent.joinpath("templates")
base_dir = Path(__file__).parent.parent.parent.parent
load_dotenv(base_dir.joinpath(".env"))

url = os.getenv("BASE_URL")
url_endpoint = "/api/users/verifyEmail/"
base_url = url + url_endpoint

class EmailSchema(BaseModel):
    email: List[EmailStr]

class MailConfiguration:
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_FROM = os.getenv("MAIL_FROM")
    MAIL_PORT = os.getenv("MAIL_PORT")
    MAIL_SERVER = os.getenv("MAIL_SERVER")

conf = ConnectionConfig(
    MAIL_USERNAME = MailConfiguration.MAIL_USERNAME,
    MAIL_PASSWORD = MailConfiguration.MAIL_PASSWORD,
    MAIL_FROM = MailConfiguration.MAIL_FROM,
    MAIL_PORT = MailConfiguration.MAIL_PORT,
    MAIL_SERVER = MailConfiguration.MAIL_SERVER,
    MAIL_STARTTLS = False,
    MAIL_SSL_TLS = True,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

def send_confirmation_email(background_tasks: BackgroundTasks, email_address: str, fullname: str, totp: str) -> JSONResponse:
    data = EmailSchema(email=[email_address])
    
    template="""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                /* Reset styles */
                body, html {
                    margin: 0;
                    padding: 0;
                }
                /* Make the email background white */
                body {
                    background-color: white;
                    font-family: Arial, sans-serif;
                }
                /* Container for the email content */
                .container {
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                    text-align: center;
                }
                /* Button style */
                .button {
                    display: inline-block;
                    background-color: #007bff;
                    color: white;
                    text-decoration: none;
                    padding: 10px 20px;
                    border-radius: 5px;
                }
                /* Responsive styles */
                @media screen and (max-width: 600px) {
                    .container {
                        padding: 10px;
                    }
                    .button {
                        display: block;
                        margin: 0 auto;
                    }
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Vui lòng xác nhận địa chỉ email</h2>
                <p>Xin chào, %s. Hãy click vào nút bên dưới để xác nhận địa chỉ email của bạn</p>
                <a href="%s" target="_blank" class="button">Xác nhận</a>
            </div>
        </body>
        </html>
    """ % (fullname, base_url + "?email=" + email_address + "&totp=" + totp)

    message = MessageSchema(
        subject="Xác nhận địa chỉ email",
        recipients=data.dict().get("email"),
        body=template,
        subtype=MessageType.html
    )

    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, message)
    return JSONResponse(content="Email has been sent", status_code=200)

def send_forget_password_email(background_tasks: BackgroundTasks, email_address: str, fullname: str, totp: str) -> JSONResponse:
    data = EmailSchema(email=[email_address])
    
    template="""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                /* Reset styles */
                body, html {
                    margin: 0;
                    padding: 0;
                }
                /* Make the email background white */
                body {
                    background-color: white;
                    font-family: Arial, sans-serif;
                }
                /* Container for the email content */
                .container {
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                    text-align: center;
                }
                /* Button style */
                .button {
                    display: inline-block;
                    background-color: white;
                    color: blue;
                    text-decoration: none;
                    font-weight: bold;
                    padding: 10px 20px;
                    border-radius: 5px;
                    font-size: 25px;
                }
                /* Responsive styles */
                @media screen and (max-width: 600px) {
                    .container {
                        padding: 10px;
                    }
                    .button {
                        display: block;
                        margin: 0 auto;
                    }
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Reset mật khẩu</h2>
                <p>Xin chào, %s. Chúng tôi đã nhận được yêu cầu reset mật khẩu của bạn. Vui lòng sử dụng mã OTP bên dưới để đặt lại mật khẩu</p>
                <div class="button">%s</div>
            </div>
        </body>
        </html>
    """ % (fullname, totp)

    message = MessageSchema(
        subject="Reset mật khẩu",
        recipients=data.dict().get("email"),
        body=template,
        subtype=MessageType.html
    )

    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, message)
    return JSONResponse(content="Email has been sent", status_code=200)