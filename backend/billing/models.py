from django.db import models

from memberships.models import Member
from memberships.models import MembershipPlan


class Payment(models.Model):

    PAYMENT_STATUS = [
        ("Paid", "Paid"),
        ("Pending", "Pending"),
        ("Failed", "Failed"),
    ]

    PAYMENT_METHOD = [
        ("Cash", "Cash"),
        ("UPI", "UPI"),
        ("Card", "Card"),
        ("Bank Transfer", "Bank Transfer"),
    ]

    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name="payments"
    )

    membership_plan = models.ForeignKey(
        MembershipPlan,
        on_delete=models.SET_NULL,
        null=True
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_method = models.CharField(
        max_length=50,
        choices=PAYMENT_METHOD,
        default="Cash"
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default="Paid"
    )

    payment_date = models.DateField(
        auto_now_add=True
    )

    transaction_id = models.CharField(
        max_length=100,
        blank=True
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
            f"{self.member} - ₹{self.amount}"
        )