import random

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


def generate_phrase():
    with open("words.txt", "r") as words:
        word_list = words.read().splitlines()
        return " ".join(random.choices(word_list, k=24))


def send_email(user):
    code = "".join(random.choices("0123456789", k=6))
    user.code = code
    user.save()

    subject = "Verify your email - Password Storage"
    html_message = render_to_string(
        "accounts/email/verification.html", {"user": user, "code": code}
    )

    send_mail(
        subject=subject,
        message=f"Your verification code is: {code}",
        html_message=html_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )


def send_phrase_email(user):
    subject = "IMPORTANT - Your recovery phrase"
    html_message = render_to_string(
        "accounts/email/recovery_phrase.html",
        {"user": user, "recovery_phrase": user.recovery_phrase},
    )

    send_mail(
        subject=subject,
        message=f"Your recovery phrase is: {user.recovery_phrase}\nKeep it safe and never share with anyone!",
        html_message=html_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )
