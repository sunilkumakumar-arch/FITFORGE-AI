from django.db import models

from trainers.models import Trainer
from .exercise import Exercise


class WorkoutTemplate(models.Model):

    GOAL_CHOICES = [
        ("WEIGHT_LOSS", "Weight Loss"),
        ("FAT_LOSS", "Fat Loss"),
        ("MUSCLE_GAIN", "Muscle Gain"),
        ("STRENGTH", "Strength"),
        ("GENERAL_FITNESS", "General Fitness"),
    ]

    DIFFICULTY_CHOICES = [
        ("BEGINNER", "Beginner"),
        ("INTERMEDIATE", "Intermediate"),
        ("ADVANCED", "Advanced"),
    ]

    name = models.CharField(
        max_length=150,
        unique=True,
    )

    description = models.TextField(
        blank=True,
    )

    goal = models.CharField(
        max_length=30,
        choices=GOAL_CHOICES,
    )

    difficulty = models.CharField(
        max_length=20,
        choices=DIFFICULTY_CHOICES,
        default="BEGINNER",
    )

    duration_weeks = models.PositiveIntegerField(
        default=4,
    )

    created_by = models.ForeignKey(
        Trainer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="workout_templates",
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return self.name


class WorkoutDay(models.Model):

    DAY_CHOICES = [
        ("MONDAY", "Monday"),
        ("TUESDAY", "Tuesday"),
        ("WEDNESDAY", "Wednesday"),
        ("THURSDAY", "Thursday"),
        ("FRIDAY", "Friday"),
        ("SATURDAY", "Saturday"),
        ("SUNDAY", "Sunday"),
    ]

    workout_template = models.ForeignKey(
        WorkoutTemplate,
        on_delete=models.CASCADE,
        related_name="days",
    )

    day_name = models.CharField(
        max_length=20,
        choices=DAY_CHOICES,
    )

    focus_area = models.CharField(
        max_length=100,
    )

    sort_order = models.PositiveIntegerField(
        default=1,
    )

    def __str__(self):
        return (
            f"{self.workout_template.name} - "
            f"{self.day_name}"
        )


class WorkoutExercise(models.Model):

    workout_day = models.ForeignKey(
        WorkoutDay,
        on_delete=models.CASCADE,
        related_name="exercises",
    )

    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.PROTECT,
        related_name="workout_exercises",
    )

    exercise_order = models.PositiveIntegerField(
        default=1,
    )

    sets = models.PositiveIntegerField()

    reps = models.CharField(
        max_length=20,
    )

    rest_seconds = models.PositiveIntegerField(
        default=60,
    )

    tempo = models.CharField(
        max_length=20,
        blank=True,
    )

    rpe = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    notes = models.TextField(
        blank=True,
    )

    def __str__(self):
        return (
            f"{self.workout_day} - "
            f"{self.exercise.name}"
        )