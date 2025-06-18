import smtplib
from email.message import EmailMessage
import os
from temporalio import activity
from dotenv import load_dotenv
from utils.shared import User, EmailContent

load_dotenv()


class EmailManager:
    def __init__(self):
        self.smtp_server: str = "smtp.hostinger.com"
        self.port: int = 587
        self.sender_email: str = os.getenv("senderEmail")
        self.password: str = os.getenv("senderPassword")

        if not self.sender_email or not self.password:
            raise ValueError(
                "Sender email and password must be set in environment variables."
            )

    # Email sender funtion, its done to use hostinger since it doesnt require 2f to test, using the smtp_server of it
    @activity.defn
    async def send_email(self, email_data: EmailContent) -> str:
        msg = EmailMessage()
        msg["Subject"] = "Test Email"
        msg["From"] = self.sender_email
        msg["To"] = email_data.user.email

        msg.set_content(email_data.message)

        try:
            with smtplib.SMTP(self.smtp_server, self.port) as server:
                server.starttls()  # Secure the connection
                server.login(self.sender_email, self.password)
                server.send_message(msg)

        except Exception as e:
            return str(e)

        return "Email sent successfully"

    # Email verify funtion, its done to use hostinger since it doesnt require 2f to test, using the smtp_server of it and a dummy message
    @activity.defn
    async def verify_email(self, user_data: User) -> str:
        message = "This is a verification test :D"
        email_data = EmailContent(user=user_data, message=message)
        status = await self.send_email(email_data)

        return status
