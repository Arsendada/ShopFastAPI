import asyncio

from app.services.emails.email import send_reset_password_email, send_new_account_email
from app.services.tasks.worker import celery_app


@celery_app.task(name="send_email_register")
def task_send_new_account(
        email_to: str,
        username: str,
        token: str
) -> bool:
    asyncio.run(send_new_account_email(
        email_to=email_to,
        username=username,
        token=token
    ))
    return True


@celery_app.task(name="send_password_register")
def task_send_password_reset(
        email_to: str,
        username: str,
        token: str
) -> bool:
    asyncio.run(send_reset_password_email(
        email_to=email_to,
        username=username,
        token=token
    ))
    return True


@celery_app.task(name="test_task")
def test_celery_start(*args) -> str:
    return f"{args}"
