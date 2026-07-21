from .models import Payment


class PaymentService:
    """
    Handles all payment-related business logic.
    This is the single place where Payment records
    should be created.
    """

    @staticmethod
    def create_payment(
        *,
        member,
        membership_plan,
        amount,
        payment_method="Cash",
        payment_status="Paid",
        transaction_id="",
        notes="",
    ):
        return Payment.objects.create(
            member=member,
            membership_plan=membership_plan,
            amount=amount,
            payment_method=payment_method,
            payment_status=payment_status,
            transaction_id=transaction_id,
            notes=notes,
        )