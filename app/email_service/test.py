from app.core.config import settings

from .base import EmailTemplate, send_email


def send_test_email(email_to: str) -> None:
    subject = f"{settings.PROJECT_NAME} - Test email"
    template_str = EmailTemplate.TEST.file()
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={"email": email_to},
    )
