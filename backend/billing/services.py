from decimal import Decimal

from django.db import transaction
from django.utils import timezone

from audit.services import AuditService

from .models import Payment


class PaymentService:
    """
    Enterprise Billing Service.

    Every payment in FitForge must be created
    through this service.
    """

    @staticmethod
    def generate_payment_number():

        last_payment = (
            Payment.objects
            .order_by("-id")
            .first()
        )

        if not last_payment:
            return "PAY000001"

        if not last_payment.payment_number:
            return f"PAY{last_payment.id + 1:06d}"

        last_number = int(
            last_payment.payment_number.replace(
                "PAY",
                ""
            )
        )

        return f"PAY{last_number + 1:06d}"

    @staticmethod
    def generate_invoice_number():

        last_payment = (
            Payment.objects
            .order_by("-id")
            .first()
        )

        if not last_payment:
            return "INV000001"

        if not last_payment.invoice_number:
            return f"INV{last_payment.id + 1:06d}"

        last_number = int(
            last_payment.invoice_number.replace(
                "INV",
                ""
            )
        )

        return f"INV{last_number + 1:06d}"

    @staticmethod
    def generate_receipt_number():

        last_payment = (
            Payment.objects
            .order_by("-id")
            .first()
        )

        if not last_payment:
            return "RCPT000001"

        if not last_payment.receipt_number:
            return f"RCPT{last_payment.id + 1:06d}"

        last_number = int(
            last_payment.receipt_number.replace(
                "RCPT",
                ""
            )
        )

        return f"RCPT{last_number + 1:06d}"

    @staticmethod
    def calculate_final_amount(
        amount,
        discount,
        tax,
    ):

        amount = Decimal(amount)
        discount = Decimal(discount)
        tax = Decimal(tax)

        final_amount = amount - discount + tax

        if final_amount < 0:
            raise ValueError(
                "Final amount cannot be negative."
            )

        return final_amount

    @staticmethod
    @transaction.atomic
    def create_payment(
        *,
        member,
        membership=None,
        collected_by=None,
        amount,
        discount=0,
        tax=0,
        payment_method="CASH",
        payment_status="COMPLETED",
        payment_date=None,
        transaction_id="",
        notes="",
    ):

        final_amount = PaymentService.calculate_final_amount(
            amount,
            discount,
            tax,
        )

        if payment_date is None:
            payment_date = timezone.localdate()

        payment = Payment.objects.create(
            payment_number=PaymentService.generate_payment_number(),
            invoice_number=PaymentService.generate_invoice_number(),
            receipt_number=PaymentService.generate_receipt_number(),

            organization=membership.plan.organization if membership else None,
            branch=membership.plan.branch if membership else None,

            member=member,
            membership=membership,
            collected_by=collected_by,

            amount=amount,
            discount=discount,
            tax=tax,
            final_amount=final_amount,

            payment_method=payment_method,
            payment_status=payment_status,
            payment_date=payment_date,

            transaction_id=transaction_id,
            notes=notes,
        )

        AuditService.log(
            user=(
                collected_by.user
                if collected_by and collected_by.user
                else None
            ),
            action="CREATE",
            module="PAYMENT",
            object_id=str(payment.id),
            object_name=payment.payment_number,
            description=(
                f"Payment {payment.payment_number} "
                f"created successfully."
            ),
        )

        return payment