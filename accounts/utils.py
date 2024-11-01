import random

from django.conf import settings
from django.core.mail import send_mail


def generate_phrase():
    with open("words.txt", "r") as words:
        word_list = words.read().splitlines()
        return " ".join(random.choices(word_list, k=random.randint(24)))


def send_email(user):
    code = "".join(random.choices("0123456789", k=6))
    user.code = code
    user.save()

    subject = "Verify your email - Password Storage"
    message = f"Your verification code is {code}"

    send_email(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )
