from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from accounts.models import Member
from trainers.models import Trainer
from roles.models import Role, Permission
from workouts.models import (
    WorkoutTemplate,
    WorkoutDay,
    MemberWorkoutPlan,
    MemberWorkoutDay,
)


User = get_user_model()


class WorkoutAssignmentAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            username="workout_assignment_api_user",
            password="TestPassword123!",
        )

        self.member = Member.objects.create(
            first_name="API",
            last_name="Workout Member",
            phone="9999994001",
            email="workout.assignment.api@example.com",
            gender="Male",
            date_of_birth=date(1995, 1, 1),
        )

        self.trainer = Trainer.objects.create(
            first_name="API",
            last_name="Trainer",
            phone="9999994002",
            email="workout.assignment.trainer@example.com",
            employment_status="Active",
        )

        self.organization = None
        self.branch = None

        self.view_permission = Permission.objects.create(
            module="workout",
            code="workout.view",
            name="View Workout Assignments",
            is_active=True,
        )

        self.create_permission = Permission.objects.create(
            module="workout",
            code="workout.create",
            name="Create Workout Assignments",
            is_active=True,
        )

        self.update_permission = Permission.objects.create(
            module="workout",
            code="workout.update",
            name="Update Workout Assignments",
            is_active=True,
        )

        self.role = Role.objects.create(
            code="TEST_WORKOUT_ASSIGNMENT_API",
            name="Test Workout Assignment API Role",
            is_active=True,
        )

        self.employee = self._create_employee()

        self.template = WorkoutTemplate.objects.create(
            name="API Assignment Template",
            goal="MUSCLE_GAIN",
            difficulty="INTERMEDIATE",
            duration_weeks=8,
            created_by=self.trainer,
        )

        self.day1 = WorkoutDay.objects.create(
            workout_template=self.template,
            day_name="MONDAY",
            focus_area="Chest",
            sort_order=1,
        )

        self.day2 = WorkoutDay.objects.create(
            workout_template=self.template,
            day_name="WEDNESDAY",
            focus_area="Back",
            sort_order=2,
        )

    def _create_employee(self):
        from core.models import Organization, Branch
        from employees.models import Employee

        organization = Organization.objects.create(
            name="Workout Assignment API Organization",
            owner_name="Test Owner",
            email="workout.assignment.organization@example.com",
            phone="9999994003",
        )

        branch = Branch.objects.create(
            organization=organization,
            name="Workout Assignment API Branch",
            city="Hyderabad",
            address="Test Address",
        )

        self.organization = organization
        self.branch = branch

        return Employee.objects.create(
            employee_code="TESTWKTASSIGN001",
            user=self.user,
            first_name="Workout",
            last_name="Assignment Tester",
            email="workout.assignment.employee@example.com",
            phone="9999994004",
            organization=organization,
            branch=branch,
            joining_date=date.today(),
            employment_status="ACTIVE",
            role=self.role,
        )

    # =====================================================
    # LIST
    # =====================================================

    def test_unauthenticated_user_cannot_list_member_plans(self):
        response = self.client.get(
            "/api/v1/workouts/member-plans/"
        )

        self.assertIn(
            response.status_code,
            [401, 403],
        )

    def test_employee_without_view_permission_cannot_list_member_plans(self):
        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.get(
            "/api/v1/workouts/member-plans/"
        )

        self.assertEqual(
            response.status_code,
            403,
        )

    def test_employee_with_view_permission_can_list_member_plans(self):
        self.role.permissions.add(
            self.view_permission
        )

        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.get(
            "/api/v1/workouts/member-plans/"
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    # =====================================================
    # CREATE / ASSIGN
    # =====================================================

    def test_employee_without_create_permission_cannot_assign_plan(self):
        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.post(
            "/api/v1/workouts/member-plans/",
            {
                "member": self.member.id,
                "workout_template": self.template.id,
                "trainer": self.trainer.id,
                "assignment_type": "GENERAL",
                "source": "TEMPLATE",
                "start_date": str(date.today()),
                "notes": "API assignment test.",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            403,
        )

        self.assertFalse(
            MemberWorkoutPlan.objects.filter(
                member=self.member,
                workout_template=self.template,
            ).exists()
        )

    def test_employee_with_create_permission_can_assign_plan(self):
        self.role.permissions.add(
            self.create_permission
        )

        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.post(
            "/api/v1/workouts/member-plans/",
            {
                "member": self.member.id,
                "workout_template": self.template.id,
                "trainer": self.trainer.id,
                "assignment_type": "GENERAL",
                "source": "TEMPLATE",
                "start_date": str(date.today()),
                "notes": "API assignment test.",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            201,
        )

        plan = MemberWorkoutPlan.objects.get(
            member=self.member,
            workout_template=self.template,
        )

        self.assertEqual(
            plan.assigned_by,
            self.user,
        )

        self.assertEqual(
            plan.status,
            "ACTIVE",
        )

        self.assertEqual(
            plan.version,
            1,
        )

        self.assertEqual(
            MemberWorkoutDay.objects.filter(
                member_workout=plan
            ).count(),
            2,
        )

    def test_employee_with_create_permission_cannot_assign_second_active_plan(self):
        self.role.permissions.add(
            self.create_permission
        )

        self.client.force_authenticate(
            user=self.user
        )

        first_response = self.client.post(
            "/api/v1/workouts/member-plans/",
            {
                "member": self.member.id,
                "workout_template": self.template.id,
                "trainer": self.trainer.id,
                "assignment_type": "GENERAL",
                "source": "TEMPLATE",
                "start_date": str(date.today()),
            },
            format="json",
        )

        self.assertEqual(
            first_response.status_code,
            201,
        )

        second_response = self.client.post(
            "/api/v1/workouts/member-plans/",
            {
                "member": self.member.id,
                "workout_template": self.template.id,
                "trainer": self.trainer.id,
                "assignment_type": "GENERAL",
                "source": "TEMPLATE",
                "start_date": str(date.today()),
            },
            format="json",
        )

        self.assertEqual(
            second_response.status_code,
            400,
        )

        self.assertEqual(
            MemberWorkoutPlan.objects.filter(
                member=self.member
            ).count(),
            1,
        )

    # =====================================================
    # COMPLETE
    # =====================================================

    def test_employee_without_update_permission_cannot_complete_plan(self):
        self.role.permissions.add(
            self.create_permission
        )

        self.client.force_authenticate(
            user=self.user
        )

        create_response = self.client.post(
            "/api/v1/workouts/member-plans/",
            {
                "member": self.member.id,
                "workout_template": self.template.id,
                "trainer": self.trainer.id,
                "assignment_type": "GENERAL",
                "source": "TEMPLATE",
                "start_date": str(date.today()),
            },
            format="json",
        )

        self.assertEqual(
            create_response.status_code,
            201,
        )

        plan = MemberWorkoutPlan.objects.get(
            member=self.member
        )

        response = self.client.post(
            f"/api/v1/workouts/member-plans/{plan.id}/complete/",
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            403,
        )

    def test_employee_with_update_permission_can_complete_plan(self):
        self.role.permissions.add(
            self.create_permission,
            self.update_permission,
        )

        self.client.force_authenticate(
            user=self.user
        )

        create_response = self.client.post(
            "/api/v1/workouts/member-plans/",
            {
                "member": self.member.id,
                "workout_template": self.template.id,
                "trainer": self.trainer.id,
                "assignment_type": "GENERAL",
                "source": "TEMPLATE",
                "start_date": str(date.today()),
            },
            format="json",
        )

        self.assertEqual(
            create_response.status_code,
            201,
        )

        plan = MemberWorkoutPlan.objects.get(
            member=self.member
        )

        response = self.client.post(
            f"/api/v1/workouts/member-plans/{plan.id}/complete/",
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        plan.refresh_from_db()

        self.assertEqual(
            plan.status,
            "COMPLETED",
        )

        self.assertEqual(
            plan.end_date,
            date.today(),
        )

    # =====================================================
    # CANCEL
    # =====================================================

    def test_employee_without_update_permission_cannot_cancel_plan(self):
        self.role.permissions.add(
            self.create_permission
        )

        self.client.force_authenticate(
            user=self.user
        )

        create_response = self.client.post(
            "/api/v1/workouts/member-plans/",
            {
                "member": self.member.id,
                "workout_template": self.template.id,
                "trainer": self.trainer.id,
                "assignment_type": "GENERAL",
                "source": "TEMPLATE",
                "start_date": str(date.today()),
            },
            format="json",
        )

        self.assertEqual(
            create_response.status_code,
            201,
        )

        plan = MemberWorkoutPlan.objects.get(
            member=self.member
        )

        response = self.client.post(
            f"/api/v1/workouts/member-plans/{plan.id}/cancel/",
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            403,
        )

    def test_employee_with_update_permission_can_cancel_plan(self):
        self.role.permissions.add(
            self.create_permission,
            self.update_permission,
        )

        self.client.force_authenticate(
            user=self.user
        )

        create_response = self.client.post(
            "/api/v1/workouts/member-plans/",
            {
                "member": self.member.id,
                "workout_template": self.template.id,
                "trainer": self.trainer.id,
                "assignment_type": "GENERAL",
                "source": "TEMPLATE",
                "start_date": str(date.today()),
            },
            format="json",
        )

        self.assertEqual(
            create_response.status_code,
            201,
        )

        plan = MemberWorkoutPlan.objects.get(
            member=self.member
        )

        response = self.client.post(
            f"/api/v1/workouts/member-plans/{plan.id}/cancel/",
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        plan.refresh_from_db()

        self.assertEqual(
            plan.status,
            "CANCELLED",
        )

        self.assertEqual(
            plan.end_date,
            date.today(),
        )