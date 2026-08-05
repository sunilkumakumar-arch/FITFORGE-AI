from datetime import timedelta

from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from billing.services import PaymentService

from .models import MemberPTPackage
from .selectors import PTPackageSelector

from trainers.models import Trainer
from trainer_assignments.models import TrainerAssignment


class PTPackagePurchaseService:

    @staticmethod
    @transaction.atomic
    def purchase_package(
        *,
        member,
        package,
        amount_paid,
        payment_method="Cash",
        transaction_id="",
        notes="PT Package Purchase",
    ):

        active_membership = (
            PTPackageSelector.get_active_membership(member)
        )

        if not active_membership:
            raise ValidationError(
                "Active membership required before purchasing a PT Package."
            )

        membership_remaining_days = (
            PTPackageSelector.membership_remaining_days(
                active_membership
            )
        )

        if membership_remaining_days <= 0:
            raise ValidationError(
                "Membership has expired. Renew membership first."
            )

        active_package = (
            PTPackageSelector.get_active_pt_package(member)
        )

        if active_package:

            remaining_sessions = (
                PTPackageSelector.package_remaining_sessions(
                    active_package
                )
            )

            remaining_days = (
                PTPackageSelector.package_remaining_days(
                    active_package
                )
            )

            if (
                remaining_sessions > 3
                and remaining_days > 15
            ):
                raise ValidationError(
                    f"Active PT Package already exists. Remaining Sessions: "
                    f"{remaining_sessions}, Remaining Days: {remaining_days}"
                )

        purchase_date = timezone.now().date()

        expiry_date = (
            purchase_date +
            timedelta(days=package.validity_days)
        )

        if expiry_date > active_membership.end_date:
            expiry_date = active_membership.end_date

        member_package = (
            MemberPTPackage.objects.create(
                member=member,
                trainer_assignment=None,
                package=package,
                purchase_date=purchase_date,
                expiry_date=expiry_date,
                sessions_used=0,
                is_active=True,
            )
        )

        PaymentService.create_payment(
            member=member,
            membership_plan=None,
            amount=amount_paid,
            payment_method=payment_method,
            transaction_id=transaction_id,
            notes=notes,
        )

        return member_package




class PTTrainerAssignmentService:

    @staticmethod
    @transaction.atomic
    def assign_trainer(
        *,
        member_package,
        trainer,
    ):

        trainer_assignment = TrainerAssignment.objects.create(
            member=member_package.member,
            trainer=trainer,
            start_date=member_package.purchase_date,
            end_date=member_package.expiry_date,
            monthly_fee=0,
            sessions_per_week=0,
        )

        member_package.trainer_assignment = trainer_assignment
        member_package.save(update_fields=["trainer_assignment"])

        return trainer_assignment    