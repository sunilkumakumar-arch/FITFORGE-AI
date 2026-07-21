from django.db import transaction
from django.utils import timezone

from .models import MemberMembership
from billing.services import PaymentService


class MembershipPurchaseService:
    """
    Handles the complete membership purchase workflow.
    """

    @staticmethod
    @transaction.atomic
    def purchase_membership(
        *,
        member,
        plan,
        start_date,
        amount_paid,
        payment_method="Cash",
        transaction_id="",
        notes="Membership Purchase",
    ):
        
        print("\n========== PURCHASE MEMBERSHIP ==========")
        print(f"Member: {member.id}")
        print(f"Plan: {plan.id}")
        print(f"Start Date: {start_date}")
        print(f"Amount Paid: {amount_paid}")

        active_membership = (
            MemberMembership.objects
            .filter(
                member=member,
                status="Active"
            )
            .order_by("-end_date")
            .first()
        )

        if active_membership:

            remaining_days = (
                active_membership.end_date -
                timezone.now().date()
            ).days

            if remaining_days > 15:
                raise ValueError(
                    f"Member already has an active membership. Remaining days: {remaining_days}"
                )

        membership = MemberMembership.objects.create(
            member=member,
            plan=plan,
            start_date=start_date,
            amount_paid=amount_paid,
            payment_reference=transaction_id,
            status="Active",
        )
        print(f"Saved Membership ID: {membership.id}")

        PaymentService.create_payment(
            member=member,
            membership_plan=plan,
            amount=amount_paid,
            payment_method=payment_method,
            payment_status="Paid",
            transaction_id=transaction_id,
            notes=notes,
        )

        return membership