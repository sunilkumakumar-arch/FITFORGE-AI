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
        fields = "__all__"


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
        fields = "__all__"