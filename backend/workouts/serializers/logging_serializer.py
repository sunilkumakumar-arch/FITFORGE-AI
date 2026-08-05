from rest_framework import serializers

from workouts.models import (
    WorkoutLog,
    ExerciseLog,
)


class ExerciseLogSerializer(serializers.ModelSerializer):

    exercise_name = serializers.CharField(
        source="workout_exercise.exercise.name",
        read_only=True,
    )

    class Meta:
        model = ExerciseLog
        fields = "__all__"


class WorkoutLogSerializer(serializers.ModelSerializer):

    exercises = ExerciseLogSerializer(
        source="exercise_logs",
        many=True,
        read_only=True,
    )

    member_name = serializers.CharField(
        source="member_workout.member.first_name",
        read_only=True,
    )

    class Meta:
        model = WorkoutLog
        fields = "__all__"