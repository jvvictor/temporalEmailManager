import asyncio
import logging

import sys
import os

sys.path.append(os.getcwd())

from utils.emailUtils import emailManager
from temporalUtils.workflows import sendEmailWorkflow, sendVerifyEmailWorkflow

from temporalio.client import Client
from temporalio.worker import Worker

async def main():

    logging.basicConfig(level=logging.INFO)
    client = await Client.connect("localhost:7233", namespace="default")

    emailActivities = emailManager()

    emailWorker = Worker(
            client,
            task_queue="emails-tasks-send",
            workflows=[sendEmailWorkflow],
            activities=[emailActivities.sendEmail],
        )
    
    verifyWorker = Worker(
            client,
            task_queue="emails-tasks-verify",
            workflows=[sendVerifyEmailWorkflow],
            activities=[emailActivities.verifyEmail],
        )
    
    logging.info(f"Starting the worker....{client.identity}")

    await asyncio.gather(
        emailWorker.run(),
        verifyWorker.run(),
    )

if __name__ == "__main__":
    asyncio.run(main())