from temporalio import workflow
from datetime import timedelta

import sys
import os

# Import activity, passing it through the sandbox without reloading the module
with workflow.unsafe.imports_passed_through():
    from utils.emailUtils import EmailManager
    from utils.shared import User, EmailContent

sys.path.append(os.getcwd())


# Email sender worflow, receives a EmailContent type and send a email using the .env email
@workflow.defn
class SendEmailWorkflow:
    @workflow.run
    async def send_email(self, email_data: EmailContent) -> str:
        workflow.logger.info(f"EmailSender workflow invoked with {input}")

        email_response = await workflow.execute_activity_method(
            EmailManager.send_email,
            email_data,
            start_to_close_timeout=timedelta(seconds=5),
        )

        workflow.logger.info(f"EmailSender responded with {email_response}")

        return email_response


# Email verifier worflow, sends a dummy email to recieved User to simulate a confirmation email, using the .env email
@workflow.defn
class SendVerifyEmailWorkflow:
    @workflow.run
    async def send_verify_email(self, input: User) -> str:
        workflow.logger.info(f"EmailVerify workflow invoked with {input}")

        email_response = await workflow.execute_activity_method(
            EmailManager.verify_email,
            input,
            start_to_close_timeout=timedelta(seconds=5),
        )

        workflow.logger.info(f"EmailVerify responded with {email_response}")

        return email_response
