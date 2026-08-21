from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from core.models import Organization, Branch
from memberships.models import MembershipPlan
from roles.models import Role, Permission
from employees.models import Employee


User = get_user_model()


class MembershipPlanAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            username="membership_plan_api_user",
            password="TestPassword123!",
        )

        self.organization = Organization.objects.create(
            name="Plan API Organization",
            owner_name="Test Owner",
            email="plan.api@example.com",
            phone="9999993000",
        )

        self.branch = Branch.objects.create(
            organization=self.organization,
            name="Plan API Branch",
            city="Hyderabad",
            address="Test Address",
        )

        self.other_branch = Branch.objects.create(
            organization=self.organization,
            name="Other Plan API Branch",
            city="Hyderabad",
            address="Other Address",
        )

        self.other_organization = Organization.objects.create(
            name="Other Plan API Organization",
            owner_name="Other Owner",
            email="other.plan.api@example.com",
            phone="9999993001",
        )

        self.other_org_branch = Branch.objects.create(
            organization=self.other_organization,
            name="Other Organization Branch",
            city="Hyderabad",
            address="Other Org Address",
        )

        self.permission = Permission.objects.create(
            module="membership",
            code="membership.view",
            name="View Membership",
            is_active=True,
        )

        self.role = Role.objects.create(
            code="TEST_MEMBERSHIP_PLAN_API",
            name="Test Membership Plan API Role",
            is_active=True,
        )

        self.role.permissions.add(
            self.permission
        )

        self.employee = Employee.objects.create(
            employee_code="TESTMEMPLAN001",
            user=self.user,
            first_name="Membership",
            last_name="Plan Tester",
            email="membership.plan.employee@example.com",
            phone="9999993002",
            organization=self.organization,
            branch=self.branch,
            joining_date="2026-01-01",
            employment_status="ACTIVE",
            role=self.role,
        )

        self.active_plan = MembershipPlan.objects.create(
            name="Monthly Fitness Plan",
            code="MONTHLY",
            organization=self.organization,
            branch=self.branch,
            duration_days=30,
            price=Decimal("3000.00"),
            joining_fee=Decimal("500.00"),
            freeze_days_allowed=5,
            pt_sessions_included=2,
            description="Monthly fitness membership.",
            is_active=True,
        )

        self.second_active_plan = MembershipPlan.objects.create(
            name="Annual Fitness Plan",
            code="ANNUAL",
            organization=self.organization,
            branch=self.other_branch,
            duration_days=365,
            price=Decimal("30000.00"),
            joining_fee=Decimal("1000.00"),
            freeze_days_allowed=30,
            pt_sessions_included=12,
            description="Annual fitness membership.",
            is_active=True,
        )

        self.inactive_plan = MembershipPlan.objects.create(
            name="Inactive Fitness Plan",
            code="INACTIVE",
            organization=self.organization,
            branch=self.branch,
            duration_days=90,
            price=Decimal("8000.00"),
            joining_fee=Decimal("500.00"),
            freeze_days_allowed=10,
            pt_sessions_included=4,
            description="Inactive membership.",
            is_active=False,
        )

        self.other_org_plan = MembershipPlan.objects.create(
            name="Other Organization Plan",
            code="OTHERORG",
            organization=self.other_organization,
            branch=self.other_org_branch,
            duration_days=60,
            price=Decimal("6000.00"),
            joining_fee=Decimal("500.00"),
            freeze_days_allowed=5,
            pt_sessions_included=3,
            description="Plan from another organization.",
            is_active=True,
        )

    def authenticate(self):
        self.client.force_authenticate(
            user=self.user
        )

    def test_unauthenticated_user_cannot_list_membership_plans(self):
        response = self.client.get(
            "/api/v1/memberships/membership-plans/"
        )

        self.assertIn(
            response.status_code,
            [401, 403],
        )

    def test_user_with_permission_can_list_membership_plans(self):
        self.authenticate()

        response = self.client.get(
            "/api/v1/memberships/membership-plans/"
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_list_returns_only_active_plans(self):
        self.authenticate()

        response = self.client.get(
            "/api/v1/memberships/membership-plans/"
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        returned_codes = [
            item["code"]
            for item in response.data["results"]
        ]

        self.assertIn(
            "MONTHLY",
            returned_codes,
        )

        self.assertIn(
            "ANNUAL",
            returned_codes,
        )

        self.assertNotIn(
            "INACTIVE",
            returned_codes,
        )

    def test_retrieve_active_membership_plan(self):
        self.authenticate()

        response = self.client.get(
            f"/api/v1/memberships/membership-plans/"
            f"{self.active_plan.id}/"
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertEqual(
            response.data["id"],
            self.active_plan.id,
        )

        self.assertEqual(
            response.data["name"],
            "Monthly Fitness Plan",
        )

        self.assertEqual(
            response.data["code"],
            "MONTHLY",
        )

    def test_retrieve_inactive_plan_returns_404(self):
        self.authenticate()

        response = self.client.get(
            f"/api/v1/memberships/membership-plans/"
            f"{self.inactive_plan.id}/"
        )

        self.assertEqual(
            response.status_code,
            404,
        )

    def test_filter_by_organization(self):
        self.authenticate()

        response = self.client.get(
            "/api/v1/memberships/membership-plans/",
            {
                "organization": self.organization.id,
            },
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        returned_codes = [
            item["code"]
            for item in response.data["results"]
        ]

        self.assertIn(
            "MONTHLY",
            returned_codes,
        )

        self.assertIn(
            "ANNUAL",
            returned_codes,
        )

        self.assertNotIn(
            "OTHERORG",
            returned_codes,
        )

    def test_filter_by_branch(self):
        self.authenticate()

        response = self.client.get(
            "/api/v1/memberships/membership-plans/",
            {
                "branch": self.branch.id,
            },
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        returned_codes = [
            item["code"]
            for item in response.data["results"]
        ]

        self.assertEqual(
            returned_codes,
            ["MONTHLY"],
        )

    def test_filter_by_duration_days(self):
        self.authenticate()

        response = self.client.get(
            "/api/v1/memberships/membership-plans/",
            {
                "duration_days": 365,
            },
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        returned_codes = [
            item["code"]
            for item in response.data["results"]
        ]

        self.assertEqual(
            returned_codes,
            ["ANNUAL"],
        )

    def test_search_by_name(self):
        self.authenticate()

        response = self.client.get(
            "/api/v1/memberships/membership-plans/",
            {
                "search": "Monthly Fitness",
            },
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        returned_codes = [
            item["code"]
            for item in response.data["results"]
        ]

        self.assertEqual(
            returned_codes,
            ["MONTHLY"],
        )

    def test_search_by_code(self):
        self.authenticate()

        response = self.client.get(
            "/api/v1/memberships/membership-plans/",
            {
                "search": "ANNUAL",
            },
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        returned_codes = [
            item["code"]
            for item in response.data["results"]
        ]

        self.assertEqual(
            returned_codes,
            ["ANNUAL"],
        )

    def test_ordering_by_price(self):
        self.authenticate()

        response = self.client.get(
            "/api/v1/memberships/membership-plans/",
            {
                "ordering": "price",
            },
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        returned_codes = [
            item["code"]
            for item in response.data["results"]
        ]

        self.assertEqual(
            returned_codes[:3],
            [
                "MONTHLY",
                "OTHERORG",
                "ANNUAL",
                
            ],
        )