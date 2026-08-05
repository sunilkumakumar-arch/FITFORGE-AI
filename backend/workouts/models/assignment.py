from django.db import models

from accounts.models import Member
from trainers.models import Trainer

from .template import WorkoutTemplate
from django.conf import settings


class MemberWorkoutPlan(models.Model):

    STATUS_CHOICES = [
        ("ACTIVE", "Active"),
        ("COMPLETED", "Completed"),
        ("CANCELLED", "Cancelled"),
        ("EXPIRED", "Expired"),
    ]

    ASSIGNMENT_TYPE = [
        ("GENERAL", "General Training"),
        ("PT", "Personal Training"),
        ("AI", "AI Generated"),
    ]

    SOURCE_CHOICES = [
        ("TEMPLATE", "Template"),
        ("TRAINER", "Trainer"),
        ("AI", "AI"),
        ("IMPORT", "Import"),
    ]

    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name="workout_plans",
    )

    workout_template = models.ForeignKey(
        WorkoutTemplate,
        on_delete=models.PROTECT,
        related_name="member_assignments",
    )

    trainer = models.ForeignKey(
        Trainer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_workout_plans",
    )

    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_workout_plan_records",
    )

    last_updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="updated_workout_plan_records",
    )

    assignment_type = models.CharField(
        max_length=20,
        choices=ASSIGNMENT_TYPE,
        default="GENERAL",
    )

    source = models.CharField(
        max_length=20,
        choices=SOURCE_CHOICES,
        default="TEMPLATE",
    )

    version = models.PositiveIntegerField(
        default=1,
    )

    start_date = models.DateField()

    end_date = models.DateField(
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="ACTIVE",
    )

    notes = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return (
            f"{self.member.full_name} - "
            f"{self.workout_template.name}"
        )


class MemberWorkoutDay(models.Model):

    member_workout = models.ForeignKey(
        MemberWorkoutPlan,
        on_delete=models.CASCADE,
        related_name="days",
    )

    workout_day = models.ForeignKey(
        "WorkoutDay",
        on_delete=models.PROTECT,
        related_name="member_days",
    )

    completed = models.BooleanField(
        default=False,
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    notes = models.TextField(
        blank=True,
    )

    def __str__(self):
        return (
            f"{self.member_workout.member.full_name} - "
            f"{self.workout_day.day_name}"
        )