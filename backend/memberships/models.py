from django.db import models
from accounts.models import Member
from django.utils import timezone
from datetime import timedelta


class MembershipPlan(models.Model):
    name = models.CharField(max_length=100)

    duration_days = models.PositiveIntegerField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
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
        related_name="memberships"
    )

    plan = models.ForeignKey(
        MembershipPlan,
        on_delete=models.CASCADE,
        related_name="member_plans"
    )

    start_date = models.DateField()

    end_date = models.DateField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Active"
    )

    amount_paid = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_reference = models.CharField(
        max_length=100,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    @property
    def remaining_days(self):
        return (
            self.end_date - timezone.now().date()
        ).days

    def save(self, *args, **kwargs):

        if not self.end_date:
            self.end_date = (
                self.start_date +
                timedelta(days=self.plan.duration_days)
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.member} - {self.plan}"