from drf_yasg import openapi  # type: ignore
from drf_yasg.views import get_schema_view  # type: ignore
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version="v1",
        descriptions="API documentation.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="dunningcamille@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
