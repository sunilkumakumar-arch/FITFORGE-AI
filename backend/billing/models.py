from django.db import models

from memberships.models import MemberMembership


class Payment(models.Model):

    PAYMENT_METHODS = [
        ("Cash", "Cash"),
        ("Card", "Card"),
        ("UPI", "UPI"),
        ("Bank Transfer", "Bank Transfer"),
    ]

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Paid", "Paid"),
        ("Refunded", "Refunded"),
    ]

    invoice_number = models.CharField(
        max_length=30,
        unique=True,
    )

    membership = models.ForeignKey(
        MemberMembership,
        on_delete=models.CASCADE,
        related_name="payments",
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    payment_method = models.CharField(
        max_length=30,
        choices=PAYMENT_METHODS,
    )

    payment_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Paid",
    )

    transaction_reference = models.CharField(
        max_length=100,
        blank=True,
    )

    payment_date = models.DateTimeField(
        auto_now_add=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.invoice_number