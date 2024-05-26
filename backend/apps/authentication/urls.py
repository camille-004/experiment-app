from django.contrib.auth.views import (
    LogoutView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
)
from django.urls import path

from .views import (
    APILoginView,
    APIRegisterView,
    ConfirmEmailView,
    CustomPasswordResetView,
    FetchCitiesView,
    LoginView,
    ProfileDetailView,
    ProfileUpdateView,
    RegisterView,
    ResendVerificationEmailView,
    UserProfileView,
)

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", ProfileDetailView.as_view(), name="profile"),
    path(
        "profile/<str:username>",
        UserProfileView.as_view(),
        name="user_profile",
    ),
    path("profile/edit/", ProfileUpdateView.as_view(), name="profile_edit"),
    path("api/register/", APIRegisterView.as_view(), name="api-register"),
    path("api/login/", APILoginView.as_view(), name="api-login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path(
        "password_reset/",
        CustomPasswordResetView.as_view(),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path(
        "confirm-email/<uidb64>/<token>",
        ConfirmEmailView.as_view(),
        name="account_confirm_email",
    ),
    path(
        "resend-verification-email/",
        ResendVerificationEmailView.as_view(),
        name="resend_verification_email",
    ),
    path("fetch-cities/", FetchCitiesView.as_view(), name="fetch_cities"),
]
