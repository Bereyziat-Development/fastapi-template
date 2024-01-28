from app.core.config import settings

from .base import EmailTemplate, send_email


def send_reset_password_email(email: str, token: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Password recovery for user {email}"
    template_str = EmailTemplate.RESET_PASSWORD.file()
    link = f"{settings.WEB_APP_URL}/reset-password?token={token}"
    send_email(
        email_to=email,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": project_name,
            "email": email,
            "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
            "link": link,
        },
    )


def send_new_account_email(email: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - New account for user {email}"
    template_str = EmailTemplate.NEW_ACCOUNT.file()
    link = settings.WEB_APP_URL
    send_email(
        email_to=email,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "email": email,
            "link": link,
        },
    )
