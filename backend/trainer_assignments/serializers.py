from rest_framework import serializers

from .models import TrainerAssignment


class TrainerAssignmentSerializer(
    serializers.ModelSerializer
):

    trainer_name = serializers.CharField(
        source="trainer.first_name",
        read_only=True
    )

    member_name = serializers.CharField(
        source="member.first_name",
        read_only=True
    )

    class Meta:
        model = TrainerAssignment
        fields = "__all__"