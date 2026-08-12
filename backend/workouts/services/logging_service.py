from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from workouts.models import (
    MemberWorkoutDay,
    WorkoutLog,
    ExerciseLog,
    WorkoutExercise,
)


class WorkoutLoggingService:
    """
    Business logic for workout logging.
    """

    # =====================================================
    # Start Workout
    # =====================================================

    @staticmethod
    @transaction.atomic
    def start_workout(
        *,
        member_workout_day,
    ):
        """
        Start a workout session.
        """

        existing_log = (
            WorkoutLog.objects.filter(
                workout_day=member_workout_day,
                workout_date=timezone.now().date(),
            ).first()
        )

        if existing_log:
            return existing_log

        return WorkoutLog.objects.create(
            member_workout=member_workout_day.member_workout,
            workout_day=member_workout_day,
            workout_date=timezone.now().date(),
            status="PARTIAL",
        )

    # =====================================================
    # Log Exercise
    # =====================================================

    @staticmethod
    @transaction.atomic
    def log_exercise(
        *,
        workout_log,
        workout_exercise,
        sets_completed,
        reps_completed,
        weight_used,
        rpe=None,
        notes="",
    ):
        """
        Save a completed exercise.
        """
        if workout_exercise.workout_day_id != (
            workout_log.workout_day.workout_day_id
        ):
            raise ValidationError(
                {
                    "exercise": (
                        "Selected exercise does not belong "
                        "to the workout being logged."
                    )
                }
            )

        existing = ExerciseLog.objects.filter(
            workout_log=workout_log,
            workout_exercise=workout_exercise,
        ).first()

        if existing:
            raise ValidationError(
                {
                    "exercise": "Exercise already logged."
                }
            )


        return ExerciseLog.objects.create(
            workout_log=workout_log,
            workout_exercise=workout_exercise,
            completed=True,
            sets_completed=sets_completed,
            reps_completed=reps_completed,
            weight_used=weight_used,
            rpe=rpe,
            rest_seconds=workout_exercise.rest_seconds,
            notes=notes,
        )

    # =====================================================
    # Complete Workout
    # =====================================================

    @staticmethod
    @transaction.atomic
    def complete_workout(
        *,
        workout_log,
        duration_minutes=0,
        calories_burned=0,
        notes="",
    ):
        """
        Complete a workout session.
        """

        workout_log.status = "COMPLETED"
        workout_log.duration_minutes = duration_minutes
        workout_log.calories_burned = calories_burned
        workout_log.notes = notes

        workout_log.save(
            update_fields=[
                "status",
                "duration_minutes",
                "calories_burned",
                "notes",
                "updated_at",
            ]
        )

        member_day = workout_log.workout_day

        member_day.completed = True
        member_day.completed_at = timezone.now()

        member_day.save(
            update_fields=[
                "completed",
                "completed_at",
            ]
        )

        return workout_log

    # =====================================================
    # Workout Volume
    # =====================================================

    @staticmethod
    def calculate_volume(workout_log):
        """
        Calculate total workout volume.

        Formula:
        Weight × Sets
        """

        volume = 0

        for log in workout_log.exercise_logs.all():

            try:
                reps = int(log.reps_completed)
            except (TypeError, ValueError):
                continue

            volume += (
                float(log.weight_used)
                * reps
                * log.sets_completed
            )

        return volume

    # =====================================================
    # Personal Record
    # =====================================================

    @staticmethod
    def detect_pr(
        *,
        member,
        exercise,
        weight_used,
    ):
        """
        Placeholder for Personal Record detection.

        V2:
        Compare against previous ExerciseLogs.
        """

        return False

    # =====================================================
    # Progress Update
    # =====================================================

    @staticmethod
    def update_progress(
        *,
        member,
    ):
        """
        Placeholder.

        V2:
        Update workout consistency,
        strength score,
        adherence,
        AI metrics.
        """

        return True