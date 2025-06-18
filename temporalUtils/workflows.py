import logging
from temporalio import workflow
from datetime import timedelta

import sys
import os

sys.path.append(os.getcwd())

# Import activity, passing it through the sandbox without reloading the module
with workflow.unsafe.imports_passed_through():
    from utils.emailUtils import emailManager
    from utils.shared import (
        User, EmailContent
    )

# Email sender worflow, receives a EmailContent type and send a email using the .env email
@workflow.defn
class sendEmailWorkflow:

    @workflow.run
    async def sendEmail(self, emailData: EmailContent) -> str:

        workflow.logger.info(f"EmailSender workflow invoked with {input}")

        emailResponse = await workflow.execute_activity_method(
            emailManager.sendEmail,
            emailData,
            start_to_close_timeout=timedelta(seconds=5),
        )

        workflow.logger.info(f"EmailSender responded with {emailResponse}")

        return emailResponse

# Email verifier worflow, sends a dummy email to recieved User to simulate a confirmation email, using the .env email
@workflow.defn
class sendVerifyEmailWorkflow:

    @workflow.run
    async def sendVerifyEmail(self, input: User) -> str:

        workflow.logger.info(f"EmailVerify workflow invoked with {input}")

        emailResponse = await workflow.execute_activity_method(
            emailManager.verifyEmail,
            input,
            start_to_close_timeout=timedelta(seconds=5),
        )

        workflow.logger.info(f"EmailVerify responded with {emailResponse}")

        return emailResponse