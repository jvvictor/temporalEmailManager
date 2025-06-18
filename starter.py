import asyncio
import sys

from utils.shared import User, EmailContent
from temporalio.client import Client
from temporalUtils.workflows import sendEmailWorkflow, sendVerifyEmailWorkflow

async def main():
    
    # Create client connected to server at the given address
    client = await Client.connect("localhost:7233", namespace="default")

    # Execute email sender workflow
    handle = await client.start_workflow(
        sendEmailWorkflow.sendEmail,
        EmailContent(user=User(name=sys.argv[1], email=sys.argv[2]), message=sys.argv[3]),
        id="email-send-tasks-example",
        task_queue="emails-tasks-send",
    )

    result = await handle.result()
    print(f"Result for sender: {result}")

    # Execute verifier workflow
    handle = await client.start_workflow(
        sendVerifyEmailWorkflow.sendVerifyEmail,
        User(name=sys.argv[1], email=sys.argv[2]),
        id="verify-tasks-example",
        task_queue="emails-tasks-verify",
    )

    result = await handle.result()
    print(f"Result for verifier: {result}")

if __name__ == "__main__":
    asyncio.run(main())