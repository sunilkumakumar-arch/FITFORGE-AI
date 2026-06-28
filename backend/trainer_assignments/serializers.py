from rest_framework import serializers

from .models import TrainerAssignment


class TrainerAssignmentSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = TrainerAssignment
        fields = "__all__"