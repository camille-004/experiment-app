from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DetailView, ListView, TemplateView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Experiment, ExperimentRun
from .serializers import ExperimentRunSerializer, ExperimentSerializer


class ExperimentViewSet(viewsets.ModelViewSet):
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet:
        user = self.request.user
        if isinstance(user, User):
            return self.queryset.filter(user=self.request.user)
        return self.queryset.none()


class ExperimentRunViewSet(viewsets.ModelViewSet):
    queryset = ExperimentRun.objects.all()
    serializer_class = ExperimentRunSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet:
        user = self.request.user
        if isinstance(user, User):
            return self.queryset.filter(experiment__user=self.request.user)
        return self.queryset.none()


class ExperimentDetailView(DetailView):
    model = Experiment
    template_name = "experiments/experiment_detail.html"
    context_object_name = "experiment"

    def get_object(self, queryset: QuerySet[Any] | None = None) -> Experiment:
        return get_object_or_404(Experiment, id=self.kwargs["pk"])


class MyExperimentsView(ListView):
    model = Experiment
    template_name = "experiments/my_experiments.html"
    context_object_name = "experiments"

    def get_queryset(self) -> QuerySet:
        user = self.request.user
        if isinstance(user, User):
            return Experiment.objects.filter(user=user).order_by("-created_at")
        return Experiment.objects.none()


class CreateExperimentView(CreateView):
    model = Experiment
    template_name = "experiments/create_experiment.html"
    fields = ["name", "description"]
    success_url = "/experiments/my-experiments/"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.user = self.request.user
        return super().form_valid(form)


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["recent_experiments"] = Experiment.objects.order_by(
            "-created_at"
        )[:12]
        return context


class WorkspaceView(LoginRequiredMixin, TemplateView):
    template_name = "experiments/workspace.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["experiments"] = Experiment.objects.filter(
            user=self.request.user
        ).order_by("-created_at")
        return context
