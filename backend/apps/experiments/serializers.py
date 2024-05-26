from rest_framework import serializers

from .models import Experiment, ExperimentRun


class ExperimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experiment
        fields = "__all__"


class ExperimentRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperimentRun
        fields = "__all__"
