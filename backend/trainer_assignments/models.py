from django.db import models

from trainers.models import Trainer
from memberships.models import Member


class TrainerAssignment(models.Model):

    trainer = models.ForeignKey(
        Trainer,
        on_delete=models.CASCADE,
        related_name="assignments"
    )

    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name="trainer_assignments"
    )

    start_date = models.DateField()

    end_date = models.DateField(
        null=True,
        blank=True
    )

    monthly_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    sessions_per_week = models.PositiveIntegerField(
        default=3
    )

    is_active = models.BooleanField(
        default=True
    )

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.member} → {self.trainer}"