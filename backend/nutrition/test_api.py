from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from core.models import Organization, Branch
from employees.models import Employee
from accounts.models import Member
from nutrition.models import (
    NutritionPlan,
    Meal,
    MemberNutritionAssignment,
)
from roles.models import Role, Permission


User = get_user_model()


class NutritionPlanAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            username="nutrition_api_user",
            password="TestPassword123!",
        )

        self.organization = Organization.objects.create(
            name="Nutrition API Organization",
            owner_name="Test Owner",
            email="nutrition.api@example.com",
            phone="9999999999",
        )

        self.branch = Branch.objects.create(
            organization=self.organization,
            name="Nutrition API Branch",
            city="Hyderabad",
            address="Test Address",
        )

        self.view_permission = Permission.objects.create(
            module="nutrition",
            code="nutrition.view",
            name="View Nutrition",
            is_active=True,
        )

        self.create_permission = Permission.objects.create(
            module="nutrition",
            code="nutrition.create",
            name="Create Nutrition",
            is_active=True,
        )

        self.role = Role.objects.create(
            code="TEST_NUTRITION_API",
            name="Test Nutrition API Role",
            is_active=True,
        )

        self.employee = Employee.objects.create(
            employee_code="TESTNUTAPI001",
            user=self.user,
            first_name="Nutrition",
            last_name="API Tester",
            email="nutrition.api.employee@example.com",
            phone="9999999998",
            organization=self.organization,
            branch=self.branch,
            joining_date=date.today(),
            employment_status="ACTIVE",
            role=self.role,
        )

    def test_unauthenticated_user_cannot_list_nutrition_plans(self):
        response = self.client.get(
            "/api/v1/nutrition/plans/"
        )

        self.assertIn(
            response.status_code,
            [401, 403],
        )

    def test_employee_with_view_permission_can_list_nutrition_plans(self):
        self.role.permissions.add(
            self.view_permission
        )

        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.get(
            "/api/v1/nutrition/plans/"
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_employee_without_view_permission_cannot_list_nutrition_plans(self):
        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.get(
            "/api/v1/nutrition/plans/"
        )

        self.assertEqual(
            response.status_code,
            403,
        )

    def test_employee_with_create_permission_can_create_nutrition_plan(self):
        self.role.permissions.add(
            self.create_permission
        )

        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.post(
            "/api/v1/nutrition/plans/",
            {
                "name": "API Muscle Gain Plan",
                "goal": "Muscle Gain",
                "calories": 2500,
                "protein": 180,
                "carbs": 280,
                "fats": 70,
                "notes": "API integration test plan.",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            201,
        )

        self.assertTrue(
            NutritionPlan.objects.filter(
                name="API Muscle Gain Plan"
            ).exists()
        )


class NutritionMealAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            username="nutrition_meal_api_user",
            password="TestPassword123!",
        )

        self.organization = Organization.objects.create(
            name="Nutrition Meal API Organization",
            owner_name="Test Owner",
            email="nutrition.meal.api@example.com",
            phone="9999999997",
        )

        self.branch = Branch.objects.create(
            organization=self.organization,
            name="Nutrition Meal API Branch",
            city="Hyderabad",
            address="Test Address",
        )

        self.view_permission = Permission.objects.create(
            module="nutrition",
            code="nutrition.view",
            name="View Nutrition Meals",
            is_active=True,
        )

        self.create_permission = Permission.objects.create(
            module="nutrition",
            code="nutrition.create",
            name="Create Nutrition Meals",
            is_active=True,
        )

        self.role = Role.objects.create(
            code="TEST_NUTRITION_MEAL_API",
            name="Test Nutrition Meal API Role",
            is_active=True,
        )

        self.employee = Employee.objects.create(
            employee_code="TESTNUTMEAL001",
            user=self.user,
            first_name="Nutrition",
            last_name="Meal Tester",
            email="nutrition.meal.employee@example.com",
            phone="9999999996",
            organization=self.organization,
            branch=self.branch,
            joining_date=date.today(),
            employment_status="ACTIVE",
            role=self.role,
        )

        self.nutrition_plan = NutritionPlan.objects.create(
            name="API Meal Test Plan",
            goal="Muscle Gain",
            calories=2500,
            protein=180,
            carbs=280,
            fats=70,
        )

    def test_employee_with_view_permission_can_list_meals(self):
        self.role.permissions.add(
            self.view_permission
        )

        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.get(
            "/api/v1/nutrition/meals/"
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_employee_without_view_permission_cannot_list_meals(self):
        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.get(
            "/api/v1/nutrition/meals/"
        )

        self.assertEqual(
            response.status_code,
            403,
        )

    def test_employee_with_create_permission_can_create_meal(self):
        self.role.permissions.add(
            self.create_permission
        )

        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.post(
            "/api/v1/nutrition/meals/",
            {
                "nutrition_plan": self.nutrition_plan.id,
                "meal_name": "Breakfast",
                "meal_time": "8:00 AM",
                "foods": "Eggs, oats and banana",
                "calories": 600,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            201,
        )

        self.assertTrue(
            Meal.objects.filter(
                nutrition_plan=self.nutrition_plan,
                meal_name="Breakfast",
            ).exists()
        )

    def test_unauthenticated_user_cannot_list_meals(self):
        response = self.client.get(
            "/api/v1/nutrition/meals/"
        )

        self.assertIn(
            response.status_code,
            [401, 403],
        )

class NutritionAssignmentAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            username="nutrition_assignment_api_user",
            password="TestPassword123!",
        )

        self.organization = Organization.objects.create(
            name="Nutrition Assignment API Organization",
            owner_name="Test Owner",
            email="nutrition.assignment.api@example.com",
            phone="9999999995",
        )

        self.branch = Branch.objects.create(
            organization=self.organization,
            name="Nutrition Assignment API Branch",
            city="Hyderabad",
            address="Test Address",
        )

        self.view_permission = Permission.objects.create(
            module="nutrition",
            code="nutrition.view",
            name="View Nutrition Assignments",
            is_active=True,
        )

        self.assign_permission = Permission.objects.create(
            module="nutrition",
            code="nutrition.assign",
            name="Assign Nutrition",
            is_active=True,
        )

        self.role = Role.objects.create(
            code="TEST_NUTRITION_ASSIGNMENT_API",
            name="Test Nutrition Assignment API Role",
            is_active=True,
        )

        self.employee = Employee.objects.create(
            employee_code="TESTNUTASSIGN001",
            user=self.user,
            first_name="Nutrition",
            last_name="Assignment Tester",
            email="nutrition.assignment.employee@example.com",
            phone="9999999994",
            organization=self.organization,
            branch=self.branch,
            joining_date=date.today(),
            employment_status="ACTIVE",
            role=self.role,
        )

        self.member = Member.objects.create(
            first_name="Assignment",
            last_name="Member",
            phone="9999999903",
            email="nutrition.assignment.member@example.com",
            gender="Male",
            date_of_birth=date(1995, 1, 1),
        )

        self.nutrition_plan = NutritionPlan.objects.create(
            name="API Assignment Test Plan",
            goal="Muscle Gain",
            calories=2500,
            protein=180,
            carbs=280,
            fats=70,
        )

    def test_employee_with_view_permission_can_list_assignments(self):
        self.role.permissions.add(
            self.view_permission
        )

        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.get(
            "/api/v1/nutrition/assignments/"
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_employee_without_view_permission_cannot_list_assignments(self):
        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.get(
            "/api/v1/nutrition/assignments/"
        )

        self.assertEqual(
            response.status_code,
            403,
        )

    def test_employee_with_assign_permission_can_assign_plan(self):
        self.role.permissions.add(
            self.assign_permission
        )

        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.post(
            "/api/v1/nutrition/assignments/",
            {
                "member": self.member.id,
                "nutrition_plan": self.nutrition_plan.id,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            201,
        )

        assignment = MemberNutritionAssignment.objects.get(
            member=self.member,
            nutrition_plan=self.nutrition_plan,
        )

        self.assertEqual(
            assignment.assigned_by_employee,
            self.employee,
        )

    def test_employee_without_assign_permission_cannot_assign_plan(self):
        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.post(
            "/api/v1/nutrition/assignments/",
            {
                "member": self.member.id,
                "nutrition_plan": self.nutrition_plan.id,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            403,
        )

        self.assertFalse(
            MemberNutritionAssignment.objects.filter(
                member=self.member,
                nutrition_plan=self.nutrition_plan,
            ).exists()
        )

    def test_unauthenticated_user_cannot_list_assignments(self):
        response = self.client.get(
            "/api/v1/nutrition/assignments/"
        )

        self.assertIn(
            response.status_code,
            [401, 403],
        )
