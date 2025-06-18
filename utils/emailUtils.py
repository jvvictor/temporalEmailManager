import smtplib
from email.message import EmailMessage
import os

from temporalio import activity

from dotenv import load_dotenv
load_dotenv()

from utils.shared import User, EmailContent

class emailManager:

    def __init__(self):

        self.smtp_server = "smtp.hostinger.com"
        self.port = 587
        self.sender_email = os.getenv("senderEmail")
        self.password = os.getenv("senderPassword")

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
    
    @activity.defn
    async def verifyEmail(self, userData: User) -> str:

        message = "This is a verification test :D"
        emailData = EmailContent(user=userData, message=message)
        status = await self.sendEmail(emailData)

        return status
