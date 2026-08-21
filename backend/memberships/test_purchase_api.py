from datetime import date
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from accounts.models import Member
from billing.models import Payment
from core.models import Organization, Branch
from employees.models import Employee
from general_training.models import GeneralTrainerAssignment
from memberships.models import MembershipPlan, MemberMembership
from roles.models import Role, Permission
from trainers.models import Trainer


User = get_user_model()


class MembershipPurchaseAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            username="membership_purchase_api_user",
            password="TestPassword123!",
        )

        self.organization = Organization.objects.create(
            name="Membership Purchase API Organization",
            owner_name="Test Owner",
            email="membership.purchase.api@example.com",
            phone="9999991000",
        )

        self.branch = Branch.objects.create(
            organization=self.organization,
            name="Membership Purchase API Branch",
            city="Hyderabad",
            address="Test Address",
        )

        self.permission = Permission.objects.create(
            module="membership",
            code="membership.create",
            name="Create Membership",
            is_active=True,
        )

        self.role = Role.objects.create(
            code="TEST_MEMBERSHIP_PURCHASE_API",
            name="Test Membership Purchase API Role",
            is_active=True,
        )

        self.employee = Employee.objects.create(
            employee_code="TESTMEMPUR001",
            user=self.user,
            first_name="Membership",
            last_name="Purchase Tester",
            email="membership.purchase.employee@example.com",
            phone="9999991001",
            organization=self.organization,
            branch=self.branch,
            joining_date=date.today(),
            employment_status="ACTIVE",
            role=self.role,
        )

        self.member = Member.objects.create(
            first_name="Purchase",
            last_name="Member",
            phone="9999991002",
            email="membership.purchase.member@example.com",
            gender="Male",
            date_of_birth=date(1995, 1, 1),
        )

        self.plan = MembershipPlan.objects.create(
            name="API Monthly Membership",
            code="APIMONTHLY",
            organization=self.organization,
            branch=self.branch,
            duration_days=30,
            price=Decimal("3000.00"),
            joining_fee=Decimal("500.00"),
            freeze_days_allowed=5,
            pt_sessions_included=2,
            description="API purchase test plan.",
            is_active=True,
        )

        self.trainer = Trainer.objects.create(
            first_name="API",
            last_name="Trainer",
            phone="9999991003",
            email="membership.api.trainer@example.com",
            employment_status="Active",
            available_for_pt=True,
            active_clients=0,
        )

    def authenticate_with_permission(self):
        self.role.permissions.add(self.permission)

        self.client.force_authenticate(
            user=self.user
        )

    def purchase_payload(self):
        return {
            "member_id": self.member.id,
            "plan_id": self.plan.id,
            "amount_paid": "3000.00",
            "payment_method": "Cash",
            "transaction_id": "API-PURCHASE-001",
            "notes": "API purchase test",
            "start_date": str(date.today()),
        }

    def test_unauthenticated_user_cannot_purchase_membership(self):
        response = self.client.post(
            "/api/v1/memberships/purchase/",
            self.purchase_payload(),
            format="json",
        )

        self.assertIn(
            response.status_code,
            [401, 403],
        )

    def test_employee_without_permission_cannot_purchase_membership(self):
        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.post(
            "/api/v1/memberships/purchase/",
            self.purchase_payload(),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            403,
        )

        self.assertFalse(
            MemberMembership.objects.filter(
                member=self.member
            ).exists()
        )

    def test_employee_with_permission_can_purchase_membership(self):
        self.authenticate_with_permission()

        response = self.client.post(
            "/api/v1/memberships/purchase/",
            self.purchase_payload(),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            201,
        )

        membership = MemberMembership.objects.get(
            member=self.member,
            plan=self.plan,
        )

        self.assertEqual(
            membership.amount_paid,
            Decimal("3000.00"),
        )

        self.assertEqual(
            membership.payment_reference,
            "API-PURCHASE-001",
        )

        self.assertEqual(
            membership.status,
            "Active",
        )

    def test_purchase_creates_payment(self):
        self.authenticate_with_permission()

        response = self.client.post(
            "/api/v1/memberships/purchase/",
            self.purchase_payload(),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            201,
        )

        membership = MemberMembership.objects.get(
            member=self.member,
            plan=self.plan,
        )

        payment = Payment.objects.get(
            membership=membership,
        )

        self.assertEqual(
            payment.amount,
            Decimal("3000.00"),
        )

        self.assertEqual(
            payment.payment_method,
            "Cash",
        )

        self.assertEqual(
            payment.payment_status,
            "COMPLETED",
        )

        self.assertEqual(
            payment.transaction_id,
            "API-PURCHASE-001",
        )

    def test_purchase_auto_assigns_general_trainer(self):
        self.authenticate_with_permission()

        response = self.client.post(
            "/api/v1/memberships/purchase/",
            self.purchase_payload(),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            201,
        )

        membership = MemberMembership.objects.get(
            member=self.member,
            plan=self.plan,
        )

        assignment = GeneralTrainerAssignment.objects.get(
            member=self.member,
            membership=membership,
        )

        self.assertEqual(
            assignment.trainer,
            self.trainer,
        )

        self.assertEqual(
            assignment.assignment_status,
            "ACTIVE",
        )

        self.assertEqual(
            assignment.assignment_mode,
            "AUTO",
        )

    def test_purchase_rejects_inactive_plan(self):
        self.plan.is_active = False
        self.plan.save(
            update_fields=["is_active"]
        )

        self.authenticate_with_permission()

        response = self.client.post(
            "/api/v1/memberships/purchase/",
            self.purchase_payload(),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            400,
        )

        self.assertFalse(
            MemberMembership.objects.filter(
                member=self.member
            ).exists()
        )

    def test_purchase_rejects_invalid_member(self):
        self.authenticate_with_permission()

        payload = self.purchase_payload()
        payload["member_id"] = 999999

        response = self.client.post(
            "/api/v1/memberships/purchase/",
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            400,
        )

        self.assertFalse(
            MemberMembership.objects.filter(
                plan=self.plan
            ).exists()
        )

    def test_purchase_requires_amount_paid(self):
        self.authenticate_with_permission()

        payload = self.purchase_payload()
        del payload["amount_paid"]

        response = self.client.post(
            "/api/v1/memberships/purchase/",
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            400,
        )

    def test_purchase_requires_payment_method(self):
        self.authenticate_with_permission()

        payload = self.purchase_payload()
        del payload["payment_method"]

        response = self.client.post(
            "/api/v1/memberships/purchase/",
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            400,
        )

    def test_purchase_accepts_optional_transaction_id_and_notes(self):
        self.authenticate_with_permission()

        payload = self.purchase_payload()
        del payload["transaction_id"]
        del payload["notes"]

        response = self.client.post(
            "/api/v1/memberships/purchase/",
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            201,
        )

        membership = MemberMembership.objects.get(
            member=self.member,
            plan=self.plan,
        )

        self.assertEqual(
            membership.payment_reference,
            "",
        )