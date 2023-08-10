from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_activation_email(to_email: str, url: str) -> None:
    context = {
        "email_verification_url": url,
    }

    email_subject = "Verify Email"
    email_body = render_to_string("email_template.html", context)
    plain_message = strip_tags(email_body)
    send_mail(
        email_subject,
        plain_message,
        settings.EMAIL_HOST_USER,
        [
            to_email,
        ],
        html_message=email_body,
    )
