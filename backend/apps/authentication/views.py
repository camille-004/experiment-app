import logging
from dataclasses import dataclass
from functools import wraps
from typing import Any

import requests
from allauth.account.models import EmailAddress
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import AnonymousUser, User
from django.contrib.auth.views import PasswordResetView
from django.db.models import QuerySet
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseRedirect,
    JsonResponse,
)
from django.http.response import HttpResponseBase
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import DetailView, UpdateView
from rest_framework import generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.request import Request
from rest_framework.response import Response

from .forms import ProfileForm, ProfilePictureForm, UserProfileForm
from .models import UserProfile
from .serializers import LoginSerializer, RegisterSerializer
from .tokens import account_activation_token
from .utils import handle_user_registration, send_verification_email

logger = logging.getLogger(__name__)
GEONAMES_USERNAME = "camille004"


def get_user_profile(user: User | AnonymousUser) -> UserProfile | None:
    if isinstance(user, User):
        return user.authentication_userprofile
    return None


class FetchCitiesView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        query = request.GET.get("query", "")
        url = f"http://api.geonames.org/searchJSON?username={settings.GEONAMES_USERNAME}&q={query}&maxRows=10&featureClass=P&style=full"  # noqa
        response = requests.get(url)
        data = response.json()
        logger.info("API URL: %s", url)
        logger.info("API Response: %s", data)
        cities = [
            {"name": city["name"], "country": city["countryName"]}
            for city in data.get("geonames", [])
        ]
        logger.info("Cities fetched: %s", cities)
        return JsonResponse(cities, safe=False)


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name: str = "auth/profile.html"
    context_object_name: str = "user"

    def get_object(self, queryset: QuerySet[Any] | None = None) -> User:
        user = self.request.user
        if isinstance(user, AnonymousUser):
            raise ValueError("User is not authenticated.")
        return user


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    second_form_class = UserProfileForm
    picture_form_class = ProfilePictureForm
    template_name = "auth/profile_edit.html"
    success_url = reverse_lazy("profile")

    def get_object(self, queryset: QuerySet[User] | None = None) -> User:
        user = self.request.user
        if isinstance(user, AnonymousUser):
            raise ValueError("User is not authenticated!")
        return user

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if not isinstance(user, AnonymousUser):
            user_profile = get_user_profile(user)
            if user_profile is not None:
                if self.request.POST:
                    context["profile_form"] = self.form_class(
                        self.request.POST, instance=user
                    )
                    context["userprofile_form"] = self.second_form_class(
                        self.request.POST, instance=user_profile
                    )
                    context["picture_form"] = self.picture_form_class(
                        self.request.POST,
                        self.request.FILES,
                        instance=user_profile,
                    )
                else:
                    context["profile_form"] = self.form_class(instance=user)
                    context["userprofile_form"] = self.second_form_class(
                        instance=user_profile
                    )
                    context["picture_form"] = self.picture_form_class(
                        instance=user_profile
                    )
                    context["location"] = (
                        user_profile.location
                    )  # Have to make sure this doesn't refresh.
        return context

    def form_valid(self, form: Any) -> HttpResponse:
        context = self.get_context_data()
        profile_form = context["profile_form"]
        userprofile_form = context["userprofile_form"]
        picture_form = context["picture_form"]
        if (
            profile_form.is_valid()
            and userprofile_form.is_valid()
            and picture_form.is_valid()
        ):
            profile_form.save()
            userprofile_form.save()
            picture_form.save()
            messages.success(
                self.request, "Your profile was successfully updated!"
            )
            return redirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class LoginView(View):
    template_name: str = "login.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, self.template_name)

    @wraps(ObtainAuthToken.post)
    def post(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        return render(
            request, self.template_name, {"error": "Invalid credentials."}
        )


class RegisterView(View):
    template_name: str = "register.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, self.template_name)

    def post(self, request: HttpRequest) -> HttpResponse:
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]

        user, error = handle_user_registration(
            username, email, password, first_name, last_name
        )

        if error:
            return render(request, self.template_name, {"error": error})
        if user:
            send_verification_email(request, user)
        return redirect("account_email_verification_sent")


@dataclass
class APIRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes: tuple = (permissions.AllowAny,)
    serializer_class: Any = RegisterSerializer


class APILoginView(ObtainAuthToken):
    serializer_class = LoginSerializer

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data["token"])  # type: ignore
        return Response({"token": token.key, "user_id": token.user_id})


class ConfirmEmailView(View):
    def get(
        self, request: HttpRequest, uidb64: str, token: str
    ) -> HttpResponse:
        try:
            uid: str = force_str(urlsafe_base64_decode(uidb64))
            user: User | None = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(
            user, token
        ):
            user.is_active = True
            user.save()
            email_address = EmailAddress.objects.get(
                user=user, email=user.email
            )
            email_address.verified = True
            email_address.save()
            return redirect("login")
        else:
            return HttpResponse("Activation link is invalid!")


class ResendVerificationEmailView(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        email: str | None = request.POST.get("email")
        try:
            user = User.objects.get(email=email)
            if not user.is_active:
                send_verification_email(request, user)
                return HttpResponse("A new verification email as been sent.")
        except User.DoesNotExist:
            pass
        return HttpResponse("Invalid email or user already verified.")

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "account/email/email_verification_sent.html")


class CustomPasswordResetView(PasswordResetView):
    email_template_name: str = "registration/password_reset_email.html"
    subject_template_name: str = "registration/password_reset_subject.txt"
    success_url: str = "/auth/password_reset/done/"

    def form_valid(self, form: Any) -> HttpResponse:
        email = form.cleaned_data.get("email")
        if email is None:
            raise ValueError("Email cannot be None.")
        print(f"Password reset requested for email: {email}")
        return super().form_valid(form)


class UserProfileView(DetailView):
    model = User
    template_name = "auth/user_profile.html"
    context_object_name = "profile_user"

    def get_object(self, queryset: QuerySet[Any] | None = None) -> User:
        return get_object_or_404(User, username=self.kwargs["username"])

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        user_profile = get_user_profile(user)
        if user_profile is not None:
            context["user_profile"] = user_profile
        return context

    def dispatch(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponseBase:
        profile_user = self.get_object()
        if profile_user == request.user:
            return HttpResponseRedirect(reverse("profile"))
        return super().dispatch(request, *args, **kwargs)
