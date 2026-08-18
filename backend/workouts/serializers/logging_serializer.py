from rest_framework import serializers

from workouts.models import (
    WorkoutLog,
    ExerciseLog,
    MemberWorkoutDay,
)


class StartWorkoutSerializer(serializers.Serializer):
    """
    Input serializer for starting a workout.
    """

    workout_day = serializers.PrimaryKeyRelatedField(
        queryset=MemberWorkoutDay.objects.select_related(
            "member_workout",
            "workout_day",
        )
    )


class ExerciseLogCreateSerializer(serializers.Serializer):
    """
    Input serializer for logging an exercise.
    """

    workout_exercise = serializers.IntegerField()

    sets_completed = serializers.IntegerField(
        min_value=1,
    )

    reps_completed = serializers.CharField(
        max_length=20,
    )

    weight_used = serializers.DecimalField(
        max_digits=6,
        decimal_places=2,
        min_value=0,
    )

    rpe = serializers.IntegerField(
        required=False,
        allow_null=True,
        min_value=1,
        max_value=10,
    )

    notes = serializers.CharField(
        required=False,
        allow_blank=True,
    )


class ExerciseLogSerializer(serializers.ModelSerializer):

    exercise_name = serializers.CharField(
        source="workout_exercise.exercise.name",
        read_only=True,
    )

    class Meta:
        model = ExerciseLog

        fields = [
            "id",
            "workout_log",
            "workout_exercise",
            "exercise_name",
            "completed",
            "sets_completed",
            "reps_completed",
            "weight_used",
            "rpe",
            "rest_seconds",
            "notes",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "workout_log",
            "completed",
            "rest_seconds",
            "created_at",
        ]


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

        fields = [
            "id",
            "member_workout",
            "workout_day",
            "workout_date",
            "status",
            "duration_minutes",
            "calories_burned",
            "notes",
            "member_name",
            "exercises",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "member_workout",
            "workout_day",
            "workout_date",
            "status",
            "member_name",
            "exercises",
            "created_at",
        ]