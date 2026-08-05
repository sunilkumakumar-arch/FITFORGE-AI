from rest_framework import serializers

from workouts.models import (
    WorkoutTemplate,
    WorkoutDay,
    WorkoutExercise,
)


class WorkoutExerciseSerializer(serializers.ModelSerializer):

    exercise_name = serializers.CharField(
        source="exercise.name",
        read_only=True,
    )

    class Meta:
        model = WorkoutExercise
        fields = "__all__"


class WorkoutDaySerializer(serializers.ModelSerializer):

    exercises = WorkoutExerciseSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = WorkoutDay
        fields = "__all__"


class WorkoutTemplateSerializer(serializers.ModelSerializer):

    days = WorkoutDaySerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = WorkoutTemplate
        fields = "__all__"