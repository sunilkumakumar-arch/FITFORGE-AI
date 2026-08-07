from django.db import models
from accounts.models import Member
from core.models import (
    Organization,
    Branch,
)
from django.utils import timezone
from datetime import timedelta


class MembershipPlan(models.Model):

    name = models.CharField(
        max_length=100,
    )

    code = models.CharField(
        max_length=30,
        unique=True,
        db_index=True,
        null=True,
        blank=True,
    )

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="membership_plans",
        null=True,
        blank=True,
    )

    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name="membership_plans",
        null=True,
        blank=True,
    )

    duration_days = models.PositiveIntegerField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    joining_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    freeze_days_allowed = models.PositiveIntegerField(
        default=0,
    )

    pt_sessions_included = models.PositiveIntegerField(
        default=0,
    )

    description = models.TextField(
        blank=True,
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

    class Meta:
        ordering = ["name"]

        unique_together = (
            "organization",
            "branch",
            "name",
        )

    def __str__(self):
        if self.code:
            return f"{self.name} ({self.code})"
        return self.name


class MemberMembership(models.Model):

    STATUS_CHOICES = [
        ("Scheduled", "Scheduled"),
        ("Active", "Active"),
        ("Expired", "Expired"),
        ("Frozen", "Frozen"),
        ("Cancelled", "Cancelled"),
    ]

    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name="memberships",
    )

    plan = models.ForeignKey(
        MembershipPlan,
        on_delete=models.CASCADE,
        related_name="member_plans",
    )

    start_date = models.DateField()

    end_date = models.DateField(
        blank=True,
        null=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Active",
    )

    amount_paid = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    payment_reference = models.CharField(
        max_length=100,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    @property
    def remaining_days(self):
        if not self.end_date:
            return None

        return (self.end_date - timezone.now().date()).days

    def save(self, *args, **kwargs):
        if not self.end_date and self.plan:
            self.end_date = (
                self.start_date +
                timedelta(days=self.plan.duration_days)
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.member} - {self.plan}"