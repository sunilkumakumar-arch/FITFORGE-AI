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


class MembershipViewSetPurchaseAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            username="membership_viewset_user",
            password="TestPassword123!",
        )

        self.organization = Organization.objects.create(
            name="ViewSet Purchase Organization",
            owner_name="Test Owner",
            email="viewset.purchase@example.com",
            phone="9999992000",
        )

        self.branch = Branch.objects.create(
            organization=self.organization,
            name="ViewSet Purchase Branch",
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
            code="TEST_MEMBERSHIP_VIEWSET",
            name="Test Membership ViewSet Role",
            is_active=True,
        )

        self.role.permissions.add(self.permission)

        self.employee = Employee.objects.create(
            employee_code="TESTMEMVS001",
            user=self.user,
            first_name="ViewSet",
            last_name="Tester",
            email="viewset.employee@example.com",
            phone="9999992001",
            organization=self.organization,
            branch=self.branch,
            joining_date=date.today(),
            employment_status="ACTIVE",
            role=self.role,
        )

        self.member = Member.objects.create(
            first_name="ViewSet",
            last_name="Member",
            phone="9999992002",
            email="viewset.member@example.com",
            gender="Male",
            date_of_birth=date(1995, 1, 1),
        )

        self.plan = MembershipPlan.objects.create(
            name="ViewSet Monthly Plan",
            code="VIEWSETMONTH",
            organization=self.organization,
            branch=self.branch,
            duration_days=30,
            price=Decimal("3000.00"),
            joining_fee=Decimal("500.00"),
            freeze_days_allowed=5,
            pt_sessions_included=2,
            description="ViewSet purchase test plan.",
            is_active=True,
        )

        self.trainer = Trainer.objects.create(
            first_name="ViewSet",
            last_name="Trainer",
            phone="9999992003",
            email="viewset.trainer@example.com",
            employment_status="Active",
            available_for_pt=True,
            active_clients=0,
        )

        self.client.force_authenticate(
            user=self.user
        )

    def payload(self):
        return {
            "member_id": self.member.id,
            "plan_id": self.plan.id,
            "amount_paid": "3000.00",
            "payment_method": "Cash",
            "transaction_id": "VIEWSET-PURCHASE-001",
            "notes": "ViewSet purchase test",
            "start_date": str(date.today()),
        }

    def test_viewset_purchase_endpoint_creates_membership(self):
        response = self.client.post(
            "/api/v1/memberships/member-memberships/purchase/",
            self.payload(),
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
            membership.status,
            "Active",
        )

        self.assertEqual(
            membership.payment_reference,
            "VIEWSET-PURCHASE-001",
        )

    def test_viewset_purchase_creates_payment(self):
        response = self.client.post(
            "/api/v1/memberships/member-memberships/purchase/",
            self.payload(),
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
            payment.payment_status,
            "COMPLETED",
        )

        self.assertEqual(
            payment.transaction_id,
            "VIEWSET-PURCHASE-001",
        )

    def test_viewset_purchase_auto_assigns_general_trainer(self):
        response = self.client.post(
            "/api/v1/memberships/member-memberships/purchase/",
            self.payload(),
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

    def test_viewset_purchase_requires_permission(self):
        self.role.permissions.clear()

        response = self.client.post(
            "/api/v1/memberships/member-memberships/purchase/",
            self.payload(),
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

    def test_viewset_purchase_rejects_inactive_plan(self):
        self.plan.is_active = False
        self.plan.save(
            update_fields=["is_active"]
        )

        response = self.client.post(
            "/api/v1/memberships/member-memberships/purchase/",
            self.payload(),
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