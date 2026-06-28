from django.db import models

from accounts.models import Member
from trainers.models import Trainer


class WorkoutPlan(models.Model):

    GOAL_CHOICES = [
        ("Weight Loss", "Weight Loss"),
        ("Muscle Gain", "Muscle Gain"),
        ("Fat Loss", "Fat Loss"),
        ("Strength", "Strength"),
        ("General Fitness", "General Fitness"),
    ]

    name = models.CharField(max_length=150)

    goal = models.CharField(
        max_length=50,
        choices=GOAL_CHOICES
    )

    description = models.TextField(blank=True)

    created_by = models.ForeignKey(
        Trainer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_workout_plans"
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class WorkoutDay(models.Model):

    DAY_CHOICES = [
        ("Monday", "Monday"),
        ("Tuesday", "Tuesday"),
        ("Wednesday", "Wednesday"),
        ("Thursday", "Thursday"),
        ("Friday", "Friday"),
        ("Saturday", "Saturday"),
        ("Sunday", "Sunday"),
    ]

    workout_plan = models.ForeignKey(
        WorkoutPlan,
        on_delete=models.CASCADE,
        related_name="days"
    )

    day_name = models.CharField(
        max_length=20,
        choices=DAY_CHOICES
    )

    focus_area = models.CharField(
        max_length=100
    )

    def __str__(self):
        return f"{self.workout_plan.name} - {self.day_name}"


class WorkoutExercise(models.Model):

    workout_day = models.ForeignKey(
        WorkoutDay,
        on_delete=models.CASCADE,
        related_name="exercises"
    )

    exercise_name = models.CharField(
        max_length=150
    )

    sets = models.PositiveIntegerField()

    reps = models.CharField(
        max_length=20
    )

    rest_seconds = models.PositiveIntegerField(
        default=60
    )

    notes = models.TextField(blank=True)

    def __str__(self):
        return self.exercise_name


class MemberWorkoutAssignment(models.Model):

    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name="workout_assignments"
    )

    workout_plan = models.ForeignKey(
        WorkoutPlan,
        on_delete=models.CASCADE,
        related_name="assigned_members"
    )

    assigned_by = models.ForeignKey(
        Trainer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    assigned_date = models.DateField(
        auto_now_add=True
    )

    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.member} - {self.workout_plan}"