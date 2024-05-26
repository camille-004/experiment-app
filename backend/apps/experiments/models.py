from django.contrib.auth.models import User
from django.db import models

STATUS_CHOICES = [
    ("pending", "Pending"),
    ("running", "Running"),
    ("completed", "Completed"),
    ("failed", "Failed"),
]


class Experiment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default="pending"
    )

    def __str__(self) -> str:
        return self.name


class ExperimentRun(models.Model):
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default="pending"
    )
    logs = models.TextField(blank=True, null=True)
    metrics = models.JSONField(blank=True, null=True)

    def __str__(self) -> str:
        return f"Run for {self.experiment.name} at {self.started_at}"
