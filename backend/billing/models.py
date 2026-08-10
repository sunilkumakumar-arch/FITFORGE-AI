from django.db import models

from accounts.models import Member
from memberships.models import MemberMembership
from employees.models import Employee
from core.models import Organization, Branch
from django.utils import timezone



class Payment(models.Model):

    PAYMENT_METHOD_CHOICES = [
        ("CASH", "Cash"),
        ("UPI", "UPI"),
        ("CREDIT_CARD", "Credit Card"),
        ("DEBIT_CARD", "Debit Card"),
        ("NET_BANKING", "Net Banking"),
        ("BANK_TRANSFER", "Bank Transfer"),
        ("CHEQUE", "Cheque"),
        ("WALLET", "Wallet"),
    ]

    PAYMENT_STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("COMPLETED", "Completed"),
        ("PARTIAL", "Partial"),
        ("FAILED", "Failed"),
        ("REFUNDED", "Refunded"),
        ("CANCELLED", "Cancelled"),
    ]

    payment_number = models.CharField(
        max_length=30,
        unique=True,
        db_index=True,
        null=True,
        blank=True,
    )

    invoice_number = models.CharField(
        max_length=30,
        unique=True,
        null=True,
        blank=True,
    )

    receipt_number = models.CharField(
        max_length=30,
        unique=True,
        null=True,
        blank=True,
    )

    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name="payments",
        null=True,
        blank=True,
    )

    branch = models.ForeignKey(
        Branch,
        on_delete=models.PROTECT,
        related_name="payments",
        null=True,
        blank=True,
    )

    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name="payments",
    )

    membership = models.ForeignKey(
        MemberMembership,
        on_delete=models.SET_NULL,
        related_name="payments",
        null=True,
        blank=True,
    )

    collected_by = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        related_name="payments_collected",
        null=True,
        blank=True,
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    tax = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    final_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )

    payment_method = models.CharField(
        max_length=30,
        choices=PAYMENT_METHOD_CHOICES,
        default="CASH",
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default="COMPLETED",
    )

    payment_date = models.DateField(
        default=timezone.localdate,
    )    

    transaction_id = models.CharField(
        max_length=150,
        blank=True,
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

    class Meta:
        ordering = ["-payment_date", "-id"]

        indexes = [
            models.Index(fields=["payment_number"]),
            models.Index(fields=["invoice_number"]),
            models.Index(fields=["receipt_number"]),
            models.Index(fields=["payment_date"]),
            models.Index(fields=["payment_status"]),
            models.Index(fields=["member"]),
            models.Index(fields=["transaction_id"]),
        ]

    def __str__(self):
        return self.payment_number or f"Payment {self.id}"


    