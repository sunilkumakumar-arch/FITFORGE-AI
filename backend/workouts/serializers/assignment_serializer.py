from rest_framework import serializers

from workouts.models import (
    MemberWorkoutPlan,
    MemberWorkoutDay,
)


class MemberWorkoutDaySerializer(serializers.ModelSerializer):

    workout_day_name = serializers.CharField(
        source="workout_day.day_name",
        read_only=True,
    )

    focus_area = serializers.CharField(
        source="workout_day.focus_area",
        read_only=True,
    )

    class Meta:
        model = MemberWorkoutDay
        fields = [
            "id",
            "member_workout",
            "workout_day",
            "workout_day_name",
            "focus_area",
            "completed",
            "completed_at",
            "notes",
        ]

        read_only_fields = [
            "id",
            "member_workout",
            "completed",
            "completed_at",
        ]


class MemberWorkoutPlanSerializer(serializers.ModelSerializer):

    member_name = serializers.CharField(
        source="member.first_name",
        read_only=True,
    )

    trainer_name = serializers.CharField(
        source="trainer.first_name",
        read_only=True,
    )

    template_name = serializers.CharField(
        source="workout_template.name",
        read_only=True,
    )

    days = MemberWorkoutDaySerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = MemberWorkoutPlan

        fields = [
            "id",
            "member",
            "member_name",
            "workout_template",
            "template_name",
            "trainer",
            "trainer_name",
            "assigned_by",
            "last_updated_by",
            "assignment_type",
            "source",
            "version",
            "start_date",
            "end_date",
            "status",
            "notes",
            "days",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "assigned_by",
            "last_updated_by",
            "version",
            "end_date",
            "status",
            "days",
            "created_at",
            "updated_at",
        ]