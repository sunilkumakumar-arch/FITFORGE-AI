from django.db import models

from .assignment import (
    MemberWorkoutPlan,
    MemberWorkoutDay,
)
from .template import WorkoutExercise


class WorkoutLog(models.Model):

    STATUS_CHOICES = [
        ("COMPLETED", "Completed"),
        ("PARTIAL", "Partial"),
        ("SKIPPED", "Skipped"),
    ]

    member_workout = models.ForeignKey(
        MemberWorkoutPlan,
        on_delete=models.CASCADE,
        related_name="workout_logs",
    )

    workout_day = models.ForeignKey(
        MemberWorkoutDay,
        on_delete=models.CASCADE,
        related_name="logs",
    )

    workout_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="COMPLETED",
    )

    duration_minutes = models.PositiveIntegerField(
        default=0,
    )

    calories_burned = models.PositiveIntegerField(
        default=0,
    )

    notes = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return (
            f"{self.member_workout.member.full_name} - "
            f"{self.workout_date}"
        )


class ExerciseLog(models.Model):

    workout_log = models.ForeignKey(
        WorkoutLog,
        on_delete=models.CASCADE,
        related_name="exercise_logs",
    )

    workout_exercise = models.ForeignKey(
        WorkoutExercise,
        on_delete=models.PROTECT,
        related_name="exercise_logs",
    )

    completed = models.BooleanField(
        default=True,
    )

    sets_completed = models.PositiveIntegerField()

    reps_completed = models.CharField(
        max_length=20,
    )

    weight_used = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0,
    )

    rpe = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    rest_seconds = models.PositiveIntegerField(
        default=60,
    )

    notes = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return (
            f"{self.workout_exercise.exercise.name}"
        )