from datetime import date, timedelta
from decimal import Decimal

from django.test import TestCase
from rest_framework.exceptions import ValidationError

from accounts.models import Member
from core.models import Organization, Branch
from memberships.models import MembershipPlan, MemberMembership
from memberships.services import MembershipPurchaseService
from trainers.models import Trainer
from general_training.models import GeneralTrainerAssignment


class MembershipPurchaseServiceTests(TestCase):

    def setUp(self):
        self.organization = Organization.objects.create(
            name="Membership Test Organization",
            owner_name="Test Owner",
            email="membership.test@example.com",
            phone="9999990001",
        )

        self.branch = Branch.objects.create(
            organization=self.organization,
            name="Membership Test Branch",
            city="Hyderabad",
            address="Test Address",
        )

        self.member = Member.objects.create(
            first_name="Membership",
            last_name="Tester",
            phone="9999990002",
            email="member.membership@example.com",
            gender="Male",
            date_of_birth=date(1995, 1, 1),
        )

        self.plan = MembershipPlan.objects.create(
            name="Test Monthly Plan",
            code="TESTMONTHLY",
            organization=self.organization,
            branch=self.branch,
            duration_days=30,
            price=Decimal("3000.00"),
            joining_fee=Decimal("500.00"),
            freeze_days_allowed=5,
            pt_sessions_included=2,
            description="Membership service test plan.",
            is_active=True,
        )

        self.trainer = Trainer.objects.create(
            first_name="Auto",
            last_name="Trainer",
            phone="9999990003",
            email="auto.trainer@example.com",
            employment_status="Active",
            available_for_pt=True,
            active_clients=0,
        )

    def test_purchase_creates_active_membership(self):
        membership = MembershipPurchaseService.purchase_membership(
            member=self.member,
            plan=self.plan,
            start_date=date.today(),
            amount_paid=Decimal("3000.00"),
            payment_method="Cash",
            transaction_id="TEST-TXN-001",
            notes="Test purchase",
        )

        self.assertIsNotNone(membership.id)

        self.assertEqual(
            membership.member,
            self.member,
        )

        self.assertEqual(
            membership.plan,
            self.plan,
        )

        self.assertEqual(
            membership.status,
            "Active",
        )

    def test_purchase_calculates_end_date_from_plan_duration(self):
        start_date = date.today()

        membership = MembershipPurchaseService.purchase_membership(
            member=self.member,
            plan=self.plan,
            start_date=start_date,
            amount_paid=Decimal("3000.00"),
            payment_method="Cash",
        )

        self.assertEqual(
            membership.end_date,
            start_date + timedelta(
                days=self.plan.duration_days
            ),
        )

    def test_purchase_schedules_new_membership_after_active_membership(self):
        first_start = date.today()

        first_membership = (
            MembershipPurchaseService.purchase_membership(
                member=self.member,
                plan=self.plan,
                start_date=first_start,
                amount_paid=Decimal("3000.00"),
                payment_method="Cash",
                transaction_id="TEST-TXN-001",
            )
        )

        second_membership = (
            MembershipPurchaseService.purchase_membership(
                member=self.member,
                plan=self.plan,
                start_date=first_start,
                amount_paid=Decimal("3000.00"),
                payment_method="Cash",
                transaction_id="TEST-TXN-002",
            )
        )

        self.assertEqual(
            first_membership.status,
            "Active",
        )

        self.assertEqual(
            second_membership.status,
            "Scheduled",
        )

        self.assertEqual(
            second_membership.start_date,
            first_membership.end_date + timedelta(days=1),
        )

    def test_purchase_records_amount_and_transaction_reference(self):
        membership = MembershipPurchaseService.purchase_membership(
            member=self.member,
            plan=self.plan,
            start_date=date.today(),
            amount_paid=Decimal("2750.00"),
            payment_method="UPI",
            transaction_id="UPI-TEST-001",
        )

        self.assertEqual(
            membership.amount_paid,
            Decimal("2750.00"),
        )

        self.assertEqual(
            membership.payment_reference,
            "UPI-TEST-001",
        )

    def test_purchase_auto_assigns_general_trainer(self):
        membership = MembershipPurchaseService.purchase_membership(
            member=self.member,
            plan=self.plan,
            start_date=date.today(),
            amount_paid=Decimal("3000.00"),
            payment_method="Cash",
        )

        self.assertTrue(
            membership.status == "Active"
        )

        self.assertTrue(
            GeneralTrainerAssignment.objects.filter(
                member=self.member,
                membership=membership,
                trainer=self.trainer,
                assignment_status="ACTIVE",
                assignment_mode="AUTO",
            ).exists()
    )

    def test_purchase_requires_available_trainer_for_active_membership(self):
        self.trainer.delete()

        with self.assertRaises(ValidationError):
            MembershipPurchaseService.purchase_membership(
                member=self.member,
                plan=self.plan,
                start_date=date.today(),
                amount_paid=Decimal("3000.00"),
                payment_method="Cash",
            )

        self.assertFalse(
            MemberMembership.objects.filter(
                member=self.member
            ).exists()
        )