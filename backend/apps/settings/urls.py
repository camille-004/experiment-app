from django.urls import path

from .views import CustomPasswordChangeView, SettingsView

urlpatterns = [
    path("", SettingsView.as_view(), name="settings"),
    path(
        "change-password/",
        CustomPasswordChangeView.as_view(),
        name="change_password",
    ),
]
