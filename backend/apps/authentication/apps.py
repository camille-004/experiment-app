from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    name = "apps.authentication"

    def ready(self) -> None:
        from . import signals  # noqa: F401
