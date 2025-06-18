import asyncio
import logging

import sys
import os

sys.path.append(os.getcwd())

from utils.emailUtils import EmailManager
from temporalUtils.workflows import SendEmailWorkflow, SendVerifyEmailWorkflow

from temporalio.client import Client
from temporalio.worker import Worker


# Initialize all workers, in this case we start a emailSender worker and a emailVerify worker
async def main():
    logging.basicConfig(level=logging.INFO)
    client = await Client.connect("localhost:7233", namespace="default")

    # Create object where activities were created
    email_activities = EmailManager()

    # Sender worker
    email_worker = Worker(
        client,
        task_queue="emails-tasks-send",
        workflows=[SendEmailWorkflow],
        activities=[email_activities.send_email],
    )

    # Verifier worker
    verify_worker = Worker(
        client,
        task_queue="emails-tasks-verify",
        workflows=[SendVerifyEmailWorkflow],
        activities=[email_activities.verify_email],
    )

    logging.info(f"Starting the worker....{client.identity}")

    # Start all workers together without locking one another
    await asyncio.gather(
        email_worker.run(),
        verify_worker.run(),
    )


if __name__ == "__main__":
    asyncio.run(main())
