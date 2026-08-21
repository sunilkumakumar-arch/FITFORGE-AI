from django.db import transaction
from django.utils import timezone

from .models import MemberMembership
from billing.services import PaymentService
from datetime import timedelta

from general_training.services import (
    GeneralTrainingService,
)


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

        membership_status = "Active"

        if active_membership:
            start_date = active_membership.end_date + timedelta(days=1)
            membership_status = "Scheduled"

        membership = MemberMembership.objects.create(
            member=member,
            plan=plan,
            start_date=start_date,
            amount_paid=amount_paid,
            payment_reference=transaction_id,
            status=membership_status,
        )
        print(f"Saved Membership ID: {membership.id}")

        PaymentService.create_payment(
            member=member,
            membership=membership,
            amount=amount_paid,
            payment_method=payment_method,
            payment_status="COMPLETED",
            transaction_id=transaction_id,
            notes=notes,
        )

        # ---------------------------------------
        # AUTO GENERAL TRAINER ASSIGNMENT
        # ---------------------------------------

        if membership.status == "Active":

            GeneralTrainingService.auto_assign_trainer(
                member=member,
                membership=membership,
            )

        return membership