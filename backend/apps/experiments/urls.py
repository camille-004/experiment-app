from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CreateExperimentView,
    ExperimentDetailView,
    ExperimentRunViewSet,
    ExperimentViewSet,
    MyExperimentsView,
    WorkspaceView,
)

router = DefaultRouter()
router.register(r"experiments", ExperimentViewSet)
router.register(r"experiment-runs", ExperimentRunViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "my-experiments/", MyExperimentsView.as_view(), name="my_experiments"
    ),
    path(
        "create-experiment/",
        CreateExperimentView.as_view(),
        name="create_experiment",
    ),
    path(
        "experiment/<int:pk>/",
        ExperimentDetailView.as_view(),
        name="experiment_detail",
    ),
    path("workspace/", WorkspaceView.as_view(), name="workspace"),
]
