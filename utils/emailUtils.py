import smtplib
from email.message import EmailMessage
import os

from temporalio import activity

from dotenv import load_dotenv
load_dotenv()

from utils.shared import User, EmailContent

class emailManager:

    def __init__(self):

        self.smtp_server: str = "smtp.hostinger.com"
        self.port: int = 587
        self.sender_email: str = os.getenv("senderEmail")
        self.password: str = os.getenv("senderPassword")

        if not self.sender_email or not self.password:
            raise ValueError("Sender email and password must be set in environment variables.")

    # Email sender funtion, its done to use hostinger since it doesnt require 2f to test, using the smtp_server of it
    @activity.defn
    async def sendEmail(self, emailData: EmailContent) -> str:
        
        msg = EmailMessage()
        msg["Subject"] = "Test Email"
        msg["From"] = self.sender_email
        msg["To"] = emailData.user.email

        msg.set_content(emailData.message)

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
    async def verifyEmail(self, userData: User) -> str:

        message = "This is a verification test :D"
        emailData = EmailContent(user=userData, message=message)
        status = await self.sendEmail(emailData)

        return status
