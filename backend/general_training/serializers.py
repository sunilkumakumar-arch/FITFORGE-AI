from rest_framework import serializers

from .models import (
    GeneralTrainerAssignment,
    GeneralTrainerChangeHistory,
)


# ==========================================================
# READ SERIALIZERS
# ==========================================================

class GeneralTrainerAssignmentSerializer(
    serializers.ModelSerializer
):

    member_name = serializers.CharField(
        source="member.full_name",
        read_only=True,
    )

    trainer_name = serializers.CharField(
        source="trainer.full_name",
        read_only=True,
    )

    membership_plan = serializers.CharField(
        source="membership.plan.name",
        read_only=True,
    )

    class Meta:

        model = GeneralTrainerAssignment

        fields = (
            "id",
            "member",
            "member_name",
            "membership",
            "membership_plan",
            "trainer",
            "trainer_name",
            "assignment_status",
            "assignment_mode",
            "start_date",
            "end_date",
            "assigned_by",
            "notes",
            "created_at",
            "updated_at",
        )

        read_only_fields = fields


class GeneralTrainerChangeHistorySerializer(
    serializers.ModelSerializer
):

    member_name = serializers.CharField(
        source="member.full_name",
        read_only=True,
    )

    old_trainer_name = serializers.CharField(
        source="old_trainer.full_name",
        read_only=True,
    )

    new_trainer_name = serializers.CharField(
        source="new_trainer.full_name",
        read_only=True,
    )

    class Meta:

        model = GeneralTrainerChangeHistory

        fields = "__all__"


# ==========================================================
# INPUT SERIALIZERS
# ==========================================================

class AssignTrainerSerializer(
    serializers.Serializer
):

    member_id = serializers.IntegerField()

    membership_id = serializers.IntegerField()

    trainer_id = serializers.IntegerField()

    notes = serializers.CharField(
        required=False,
        allow_blank=True,
    )


class AutoAssignTrainerSerializer(
    serializers.Serializer
):

    member_id = serializers.IntegerField()

    membership_id = serializers.IntegerField()


class ChangeTrainerSerializer(
    serializers.Serializer
):

    member_id = serializers.IntegerField()

    new_trainer_id = serializers.IntegerField()

    reason = serializers.CharField()

    rating = serializers.IntegerField(
        min_value=1,
        max_value=5,
    )

    comments = serializers.CharField(
        required=False,
        allow_blank=True,
    )