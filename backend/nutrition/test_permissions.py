from datetime import date

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from core.models import Organization, Branch
from accounts.models import Member
from nutrition.models import NutritionPlan, MemberNutritionAssignment
from employees.models import Employee
from roles.models import Role, Permission


User = get_user_model()


class NutritionPermissionTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            username="nutrition_test_user",
            password="TestPassword123!",
        )

        self.organization = Organization.objects.create(
            name="Nutrition Test Organization",
            owner_name="Test Owner",
            email="nutritiontest@example.com",
            phone="9999999999",
        )

        self.branch = Branch.objects.create(
            organization=self.organization,
            name="Nutrition Test Branch",
            city="Hyderabad",
            address="Test Address",
        )

        self.permission = Permission.objects.create(
            module="nutrition",
            code="nutrition.view",
            name="View Nutrition",
            description="Allows viewing nutrition data.",
            is_active=True,
        )

        self.role = Role.objects.create(
            code="TEST_NUTRITION_MANAGER",
            name="Test Nutrition Manager",
            description="Test role for nutrition permission tests.",
            is_system_role=False,
            is_active=True,
        )

        self.role.permissions.add(self.permission)

        self.employee = Employee.objects.create(
            employee_code="TESTNUT001",
            user=self.user,
            first_name="Nutrition",
            last_name="Tester",
            email="nutrition.employee@example.com",
            phone="9999999998",
            organization=self.organization,
            branch=self.branch,
            joining_date=date.today(),
            employment_status="ACTIVE",
            role=self.role,
        )

        self.assign_permission = Permission.objects.create(
            module="nutrition",
            code="nutrition.assign",
            name="Assign Nutrition",
            description="Allows assigning nutrition plans to members.",
            is_active=True,
   )

    def test_employee_with_nutrition_view_can_access_assignments(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            "/api/v1/nutrition/assignments/"
        )

        self.assertEqual(response.status_code, 200)

    def test_employee_without_nutrition_view_cannot_access_assignments(self):
        self.role.permissions.clear()

        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            "/api/v1/nutrition/assignments/"
        )

        self.assertEqual(response.status_code, 403)    

    def test_inactive_employee_cannot_access_assignments(self):
        self.employee.employment_status = "SUSPENDED"
        self.employee.save(update_fields=["employment_status"])

        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            "/api/v1/nutrition/assignments/"
        )

        self.assertEqual(response.status_code, 403)    

    def test_employee_with_inactive_role_cannot_access_assignments(self):
        self.role.is_active = False
        self.role.save(update_fields=["is_active"])

        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            "/api/v1/nutrition/assignments/"
        )

        self.assertEqual(response.status_code, 403)    


    def test_employee_with_nutrition_assign_can_assign_plan(self):
        self.role.permissions.add(self.assign_permission)

        member = Member.objects.create(
            first_name="Test",
            last_name="Member",
            phone="9999999901",
            email="nutrition.member@example.com",
            gender="Male",
            date_of_birth=date(1995, 1, 1),
        )

        nutrition_plan = NutritionPlan.objects.create(
            name="Test Muscle Gain Plan",
            goal="Muscle Gain",
            calories=2500,
            protein=180,
            carbs=280,
            fats=70,
        )

        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            "/api/v1/nutrition/assignments/",
            {
                "member": member.id,
                "nutrition_plan": nutrition_plan.id,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)

        assignment = MemberNutritionAssignment.objects.get(
            member=member,
            nutrition_plan=nutrition_plan,
        )

        self.assertEqual(
            assignment.assigned_by_employee,
            self.employee,
        )    

    def test_employee_without_nutrition_assign_cannot_assign_plan(self):
        member = Member.objects.create(
            first_name="Test",
            last_name="Member Two",
            phone="9999999902",
            email="nutrition.member2@example.com",
            gender="Male",
            date_of_birth=date(1995, 1, 1),
        )

        nutrition_plan = NutritionPlan.objects.create(
            name="Test Fat Loss Plan",
            goal="Fat Loss",
            calories=2000,
            protein=160,
            carbs=200,
            fats=60,
        )

        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            "/api/v1/nutrition/assignments/",
            {
                "member": member.id,
                "nutrition_plan": nutrition_plan.id,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 403)

        self.assertFalse(
            MemberNutritionAssignment.objects.filter(
                member=member,
                nutrition_plan=nutrition_plan,
            ).exists()
        )    