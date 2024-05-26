from allauth.account.models import EmailAddress
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .tokens import account_activation_token


def handle_user_registration(
    username: str,
    email: str,
    password: str,
    first_name: str,
    last_name: str,
) -> tuple[User | None, str | None]:
    if User.objects.filter(username=username).exists():
        return None, "Username already exists."
    if User.objects.filter(email=email).exists():
        return None, "Email already exists."

    user = User.objects.create_user(
        username=username, email=email, password=password
    )
    user.first_name = first_name
    user.last_name = last_name
    user.is_active = False
    user.save()

    email_address = EmailAddress.objects.create(
        user=user, email=email, primary=True, verified=False
    )
    email_address.save()
    return user, None


def send_verification_email(request: HttpRequest, user: User) -> None:
    current_site = get_current_site(request)
    mail_subject = "Activate your account."
    message = render_to_string(
        "account/email/email_confirmation_message.html",
        {
            "user": user,
            "domain": current_site.domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": account_activation_token.make_token(user),
        },
    )
    send_mail(mail_subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
