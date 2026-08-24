from datetime import date
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from accounts.models import Member
from core.models import Organization, Branch
from employees.models import Employee
from memberships.models import MembershipPlan, MemberMembership
from roles.models import Role, Permission


User = get_user_model()


class MemberMembershipAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            username="member_membership_api_user",
            password="TestPassword123!",
        )

        self.organization = Organization.objects.create(
            name="Member Membership API Organization",
            owner_name="Test Owner",
            email="member.membership.api@example.com",
            phone="9999994000",
        )

        self.branch = Branch.objects.create(
            organization=self.organization,
            name="Member Membership API Branch",
            city="Hyderabad",
            address="Test Address",
        )

        self.other_branch = Branch.objects.create(
            organization=self.organization,
            name="Other Member Membership Branch",
            city="Hyderabad",
            address="Other Address",
        )

        self.permission_view = Permission.objects.create(
            module="membership",
            code="membership.view",
            name="View Membership",
            is_active=True,
        )

        self.permission_create = Permission.objects.create(
            module="membership",
            code="membership.create",
            name="Create Membership",
            is_active=True,
        )

        self.permission_update = Permission.objects.create(
            module="membership",
            code="membership.update",
            name="Update Membership",
            is_active=True,
        )

        self.permission_delete = Permission.objects.create(
            module="membership",
            code="membership.delete",
            name="Delete Membership",
            is_active=True,
        )

        self.role = Role.objects.create(
            code="TEST_MEMBER_MEMBERSHIP_API",
            name="Test Member Membership API Role",
            is_active=True,
        )

        self.role.permissions.add(
            self.permission_view,
            self.permission_create,
            self.permission_update,
            self.permission_delete,
        )

        self.employee = Employee.objects.create(
            employee_code="TESTMEMBERM001",
            user=self.user,
            first_name="Member",
            last_name="Membership Tester",
            email="member.membership.employee@example.com",
            phone="9999994001",
            organization=self.organization,
            branch=self.branch,
            joining_date=date(2026, 1, 1),
            employment_status="ACTIVE",
            role=self.role,
        )

        self.member = Member.objects.create(
            member_code="TESTMEMBER001",
            first_name="John",
            last_name="Membership",
            phone="9999994002",
            email="john.membership@example.com",
            gender="Male",
            date_of_birth=date(1995, 1, 1),
        )

        self.second_member = Member.objects.create(
            member_code="TESTMEMBER002",
            first_name="Jane",
            last_name="Membership",
            phone="9999994003",
            email="jane.membership@example.com",
            gender="Female",
            date_of_birth=date(1996, 2, 2),
        )

        self.plan = MembershipPlan.objects.create(
            name="Member Monthly Plan",
            code="MEMMONTH",
            organization=self.organization,
            branch=self.branch,
            duration_days=30,
            price=Decimal("3000.00"),
            joining_fee=Decimal("500.00"),
            freeze_days_allowed=5,
            pt_sessions_included=2,
            description="Member membership API plan.",
            is_active=True,
        )

        self.second_plan = MembershipPlan.objects.create(
            name="Member Annual Plan",
            code="MEMANNUAL",
            organization=self.organization,
            branch=self.other_branch,
            duration_days=365,
            price=Decimal("30000.00"),
            joining_fee=Decimal("1000.00"),
            freeze_days_allowed=30,
            pt_sessions_included=12,
            description="Annual member membership plan.",
            is_active=True,
        )

        self.membership = MemberMembership.objects.create(
            member=self.member,
            plan=self.plan,
            start_date=date(2026, 8, 1),
            amount_paid=Decimal("3000.00"),
            payment_reference="MEMBERSHIP-001",
            status="Active",
        )

        self.second_membership = MemberMembership.objects.create(
            member=self.second_member,
            plan=self.second_plan,
            start_date=date(2026, 8, 10),
            amount_paid=Decimal("30000.00"),
            payment_reference="MEMBERSHIP-002",
            status="Expired",
        )

    def authenticate(self):
        self.client.force_authenticate(
            user=self.user
        )

    def test_unauthenticated_user_cannot_list_memberships(self):
        response = self.client.get(
            "/api/v1/memberships/member-memberships/"
        )

        self.assertIn(
            response.status_code,
            [401, 403],
        )

    def test_user_with_view_permission_can_list_memberships(self):
        self.authenticate()

        response = self.client.get(
            "/api/v1/memberships/member-memberships/"
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_list_returns_membership_data(self):
        self.authenticate()

        response = self.client.get(
            "/api/v1/memberships/member-memberships/"
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        returned_ids = [
            item["id"]
            for item in response.data["results"]
        ]

        self.assertIn(
            self.membership.id,
            returned_ids,
        )

        self.assertIn(
            self.second_membership.id,
            returned_ids,
        )

    def test_membership_response_contains_member_and_plan_names(self):
        self.authenticate()

        response = self.client.get(
            f"/api/v1/memberships/member-memberships/"
            f"{self.membership.id}/"
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertEqual(
            response.data["member_name"],
            "John Membership",
        )

        self.assertEqual(
            response.data["plan_name"],
            "Member Monthly Plan",
        )

    def test_membership_response_contains_remaining_days(self):
        self.authenticate()

        response = self.client.get(
            f"/api/v1/memberships/member-memberships/"
            f"{self.membership.id}/"
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertIsNotNone(
            response.data["remaining_days"]
        )

    def test_filter_by_member(self):
        self.authenticate()

        response = self.client.get(
            "/api/v1/memberships/member-memberships/",
            {
                "member": self.member.id,
            },
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        returned_ids = [
            item["id"]
            for item in response.data["results"]
        ]

        self.assertEqual(
            returned_ids,
            [self.membership.id],
        )

    def test_filter_by_plan(self):
        self.authenticate()

        response = self.client.get(
            "/api/v1/memberships/member-memberships/",
            {
                "plan": self.second_plan.id,
            },
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        returned_ids = [
            item["id"]
            for item in response.data["results"]
        ]

        self.assertEqual(
            returned_ids,
            [self.second_membership.id],
        )

    def test_filter_by_status(self):
        self.authenticate()

        response = self.client.get(
            "/api/v1/memberships/member-memberships/",
            {
                "status": "Active",
            },
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        returned_ids = [
            item["id"]
            for item in response.data["results"]
        ]

        self.assertEqual(
            returned_ids,
            [self.membership.id],
        )

    def test_filter_by_organization(self):
        self.authenticate()

        response = self.client.get(
            "/api/v1/memberships/member-memberships/",
            {
                "plan__organization": self.organization.id,
            },
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertEqual(
            len(response.data["results"]),
            2,
        )

    def test_filter_by_branch(self):
        self.authenticate()

        response = self.client.get(
            "/api/v1/memberships/member-memberships/",
            {
                "plan__branch": self.branch.id,
            },
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        returned_ids = [
            item["id"]
            for item in response.data["results"]
        ]

        self.assertEqual(
            returned_ids,
            [self.membership.id],
        )

    def test_search_by_member_name(self):
        self.authenticate()

        response = self.client.get(
            "/api/v1/memberships/member-memberships/",
            {
                "search": "John",
            },
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        returned_ids = [
            item["id"]
            for item in response.data["results"]
        ]

        self.assertEqual(
            returned_ids,
            [self.membership.id],
        )

    def test_search_by_payment_reference(self):
        self.authenticate()

        response = self.client.get(
            "/api/v1/memberships/member-memberships/",
            {
                "search": "MEMBERSHIP-002",
            },
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        returned_ids = [
            item["id"]
            for item in response.data["results"]
        ]

        self.assertEqual(
            returned_ids,
            [self.second_membership.id],
        )

    def test_ordering_by_amount_paid(self):
        self.authenticate()

        response = self.client.get(
            "/api/v1/memberships/member-memberships/",
            {
                "ordering": "amount_paid",
            },
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        returned_ids = [
            item["id"]
            for item in response.data["results"]
        ]

        self.assertEqual(
            returned_ids,
            [
                self.membership.id,
                self.second_membership.id,
            ],
        )

    def test_create_requires_create_permission(self):
        self.role.permissions.remove(
            self.permission_create
        )

        self.authenticate()

        response = self.client.post(
            "/api/v1/memberships/member-memberships/",
            {
                "member": self.second_member.id,
                "plan": self.plan.id,
                "start_date": "2026-09-01",
                "amount_paid": "3000.00",
                "payment_reference": "CREATE-TEST",
                "status": "Scheduled",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            403,
        )

    def test_update_requires_update_permission(self):
        self.role.permissions.remove(
            self.permission_update
        )

        self.authenticate()

        response = self.client.patch(
            f"/api/v1/memberships/member-memberships/"
            f"{self.membership.id}/",
            {
                "payment_reference": "UPDATED",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            403,
        )

    def test_delete_requires_delete_permission(self):
        self.role.permissions.remove(
            self.permission_delete
        )

        self.authenticate()

        response = self.client.delete(
            f"/api/v1/memberships/member-memberships/"
            f"{self.membership.id}/"
        )

        self.assertEqual(
            response.status_code,
            403,
        )

    def test_create_rejects_inactive_plan(self):
        inactive_plan = MembershipPlan.objects.create(
            name="Inactive Member Plan",
            code="INACTIVEMEM",
            organization=self.organization,
            branch=self.branch,
            duration_days=30,
            price=Decimal("2000.00"),
            is_active=False,
        )

        self.authenticate()

        response = self.client.post(
            "/api/v1/memberships/member-memberships/",
            {
                "member": self.second_member.id,
                "plan": inactive_plan.id,
                "start_date": "2026-09-01",
                "amount_paid": "2000.00",
                "payment_reference": "INACTIVE-PLAN",
                "status": "Scheduled",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            400,
        )

    def test_create_rejects_negative_amount(self):
        self.authenticate()

        response = self.client.post(
            "/api/v1/memberships/member-memberships/",
            {
                "member": self.second_member.id,
                "plan": self.plan.id,
                "start_date": "2026-09-01",
                "amount_paid": "-100.00",
                "payment_reference": "NEGATIVE-AMOUNT",
                "status": "Scheduled",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            400,
        )

    def test_create_rejects_end_date_before_start_date(self):
        self.authenticate()

        response = self.client.post(
            "/api/v1/memberships/member-memberships/",
            {
                "member": self.second_member.id,
                "plan": self.plan.id,
                "start_date": "2026-09-10",
                "end_date": "2026-09-01",
                "amount_paid": "3000.00",
                "payment_reference": "BAD-DATE",
                "status": "Scheduled",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            400,
        )

    def test_create_calculates_end_date_from_plan_duration(self):
        self.authenticate()

        response = self.client.post(
            "/api/v1/memberships/member-memberships/",
            {
                "member": self.second_member.id,
                "plan": self.plan.id,
                "start_date": "2026-09-01",
                "amount_paid": "3000.00",
                "payment_reference": "AUTO-END-DATE",
                "status": "Scheduled",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            201,
        )

        membership = MemberMembership.objects.get(
            payment_reference="AUTO-END-DATE"
        )

        self.assertEqual(
            membership.end_date,
            date(2026, 10, 1),
        )