from typing import List
from app.api.libs.redis import redis_client
from app.core.config import settings
from fastapi import BackgroundTasks, HTTPException, status
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType


conf = ConnectionConfig(
    MAIL_USERNAME=settings.EMAIL_USER,
    MAIL_PASSWORD=settings.EMAIL_PASS,
    MAIL_FROM=settings.EMAIL_USER,
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_FROM_NAME=settings.EMAIL_USER,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
)


async def send_email(recipients: List[str], subject: str, body: str):
    message = MessageSchema(
        recipients=recipients,
        subject=subject,
        body=body,
        subtype=MessageType.html,
    )
    fm = FastMail(conf)
    await fm.send_message(message)

    for email in recipients:
        await redis_client.set(f"email_status:{email}", "delivered")


async def track_open(token: str):
    try:
        await redis_client.set(f"email_open:{token}", "opened")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


async def track_click(token: str):
    try:
        await redis_client.set(f"email_click:{token}", "clicked")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


def send_email_background(
    background_tasks: BackgroundTasks,
    recipients: List[str],
    subject: str,
    body: str,
):
    background_tasks.add_task(send_email, recipients, subject, body)


async def send_email_with_attachment(
    recipients: List[str],
    subject: str,
    body: str,
    subtype: MessageType,
    attachment_path: str,
):
    message = MessageSchema(
        recipients=recipients,
        subject=subject,
        body=body,
        subtype=subtype,
        attachments=[attachment_path],
    )
    fm = FastMail(conf)
    await fm.send_message(message)

    for email in recipients:
        redis_client.set(f"email_status:{email}", "delivered")
