from datetime import date

from django.test import TestCase

from accounts.models import Member
from employees.models import Employee
from core.models import Organization, Branch
from nutrition.models import NutritionPlan, MemberNutritionAssignment
from roles.models import Role


class NutritionAssignmentTests(TestCase):

    def setUp(self):
        self.organization = Organization.objects.create(
            name="Assignment Test Organization",
            owner_name="Test Owner",
            email="assignmenttest@example.com",
            phone="9999999999",
        )

        self.branch = Branch.objects.create(
            organization=self.organization,
            name="Assignment Test Branch",
            city="Hyderabad",
            address="Test Address",
        )

        self.role = Role.objects.create(
            code="TEST_ASSIGNMENT_ROLE",
            name="Test Assignment Role",
            is_active=True,
        )

        self.employee = Employee.objects.create(
            employee_code="TESTASSIGN001",
            first_name="Assignment",
            last_name="Tester",
            email="assignment.employee@example.com",
            phone="9999999998",
            organization=self.organization,
            branch=self.branch,
            joining_date=date.today(),
            employment_status="ACTIVE",
            role=self.role,
        )

        self.member = Member.objects.create(
            first_name="Test",
            last_name="Member",
            phone="9999999911",
            email="assignment.member@example.com",
            gender="Male",
            date_of_birth=date(1995, 1, 1),
        )

        self.nutrition_plan = NutritionPlan.objects.create(
            name="Assignment Test Plan",
            goal="Muscle Gain",
            calories=2500,
            protein=180,
            carbs=280,
            fats=70,
        )

    def test_create_assignment_successfully(self):
        assignment = MemberNutritionAssignment.objects.create(
            member=self.member,
            nutrition_plan=self.nutrition_plan,
            assigned_by_employee=self.employee,
        )

        self.assertEqual(
            assignment.member,
            self.member,
        )

        self.assertEqual(
            assignment.nutrition_plan,
            self.nutrition_plan,
        )

        self.assertEqual(
            assignment.assigned_by_employee,
            self.employee,
        )

        self.assertTrue(assignment.active)

    def test_assignment_is_active_by_default(self):
        assignment = MemberNutritionAssignment.objects.create(
            member=self.member,
            nutrition_plan=self.nutrition_plan,
            assigned_by_employee=self.employee,
        )

        self.assertTrue(assignment.active)

    def test_assignment_date_is_created_automatically(self):
        assignment = MemberNutritionAssignment.objects.create(
            member=self.member,
            nutrition_plan=self.nutrition_plan,
            assigned_by_employee=self.employee,
        )

        self.assertEqual(
            assignment.assigned_date,
            date.today(),
        )

    def test_assignment_can_be_deactivated(self):
        assignment = MemberNutritionAssignment.objects.create(
            member=self.member,
            nutrition_plan=self.nutrition_plan,
            assigned_by_employee=self.employee,
        )

        assignment.active = False
        assignment.save(update_fields=["active"])

        assignment.refresh_from_db()

        self.assertFalse(assignment.active)

    def test_assignment_string_representation(self):
        assignment = MemberNutritionAssignment.objects.create(
            member=self.member,
            nutrition_plan=self.nutrition_plan,
            assigned_by_employee=self.employee,
        )

        self.assertEqual(
            str(assignment),
            f"{self.member} - {self.nutrition_plan}",
        )
