from django.db import models

from accounts.models import Member
from trainers.models import Trainer
from trainer_assignments.models import TrainerAssignment


class PTPackage(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    total_sessions = models.PositiveIntegerField()

    validity_days = models.PositiveIntegerField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name


class MemberPTPackage(models.Model):

    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name="pt_packages"
    )

    trainer_assignment = models.ForeignKey(
        TrainerAssignment,
        on_delete=models.SET_NULL,
        related_name="member_packages",
        null=True,
        blank=True,
    )

    package = models.ForeignKey(
        PTPackage,
        on_delete=models.CASCADE
    )

    purchase_date = models.DateField()

    expiry_date = models.DateField()

    sessions_used = models.PositiveIntegerField(
        default=0
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    @property
    def sessions_remaining(self):
        return (
            self.package.total_sessions -
            self.sessions_used
        )

    def __str__(self):
        return (
            f"{self.member} - {self.package}"
        )


class PTSession(models.Model):

    STATUS_CHOICES = [
        ("Scheduled", "Scheduled"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
        ("No Show", "No Show"),
    ]

    member_package = models.ForeignKey(
        MemberPTPackage,
        on_delete=models.CASCADE,
        related_name="sessions"
    )

    trainer = models.ForeignKey(
        Trainer,
        on_delete=models.CASCADE
    )

    session_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Scheduled"
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

    def __str__(self):
        return (
            f"{self.member_package.member} - "
            f"{self.session_date}"
        )