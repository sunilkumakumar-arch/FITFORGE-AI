from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from core.models import Organization, Branch
from employees.models import Employee
from roles.models import Role, Permission
from workouts.models import (
    WorkoutTemplate,
    WorkoutDay,
    WorkoutExercise,
    MuscleGroup,
    ExerciseCategory,
    Equipment,
    Exercise,
)


User = get_user_model()


class WorkoutTemplateAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            username="workout_template_api_user",
            password="TestPassword123!",
        )

        self.organization = Organization.objects.create(
            name="Workout Template API Organization",
            owner_name="Test Owner",
            email="workout.template.api@example.com",
            phone="9999993001",
        )

        self.branch = Branch.objects.create(
            organization=self.organization,
            name="Workout Template API Branch",
            city="Hyderabad",
            address="Test Address",
        )

        self.view_permission = Permission.objects.create(
            module="workout",
            code="workout.view",
            name="View Workouts",
            is_active=True,
        )

        self.create_permission = Permission.objects.create(
            module="workout",
            code="workout.create",
            name="Create Workouts",
            is_active=True,
        )

        self.role = Role.objects.create(
            code="TEST_WORKOUT_TEMPLATE_API",
            name="Test Workout Template API Role",
            is_active=True,
        )

        self.employee = Employee.objects.create(
            employee_code="TESTWKTEMPLATE001",
            user=self.user,
            first_name="Workout",
            last_name="Template Tester",
            email="workout.template.employee@example.com",
            phone="9999993002",
            organization=self.organization,
            branch=self.branch,
            joining_date=date.today(),
            employment_status="ACTIVE",
            role=self.role,
        )

        self.template = WorkoutTemplate.objects.create(
            name="API Template Test",
            description="Workout template API test.",
            goal="MUSCLE_GAIN",
            difficulty="INTERMEDIATE",
            duration_weeks=8,
            is_active=True,
        )

    # =====================================================
    # TEMPLATE API
    # =====================================================

    def test_unauthenticated_user_cannot_list_templates(self):
        response = self.client.get(
            "/api/v1/workouts/templates/"
        )

        self.assertIn(
            response.status_code,
            [401, 403],
        )

    def test_employee_without_view_permission_cannot_list_templates(self):
        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.get(
            "/api/v1/workouts/templates/"
        )

        self.assertEqual(
            response.status_code,
            403,
        )

    def test_employee_with_view_permission_can_list_templates(self):
        self.role.permissions.add(
            self.view_permission
        )

        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.get(
            "/api/v1/workouts/templates/"
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_employee_with_create_permission_can_create_template(self):
        self.role.permissions.add(
            self.create_permission
        )

        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.post(
            "/api/v1/workouts/templates/",
            {
                "name": "API Strength Template",
                "description": "API-created strength template.",
                "goal": "STRENGTH",
                "difficulty": "ADVANCED",
                "duration_weeks": 6,
                "is_active": True,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            201,
        )

        self.assertTrue(
            WorkoutTemplate.objects.filter(
                name="API Strength Template"
            ).exists()
        )

    # =====================================================
    # WORKOUT DAY API
    # =====================================================

    def test_employee_with_view_permission_can_list_workout_days(self):
        self.role.permissions.add(
            self.view_permission
        )

        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.get(
            "/api/v1/workouts/days/"
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_employee_without_view_permission_cannot_list_workout_days(self):
        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.get(
            "/api/v1/workouts/days/"
        )

        self.assertEqual(
            response.status_code,
            403,
        )

    def test_employee_with_create_permission_can_create_workout_day(self):
        self.role.permissions.add(
            self.create_permission
        )

        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.post(
            "/api/v1/workouts/days/",
            {
                "workout_template": self.template.id,
                "day_name": "MONDAY",
                "focus_area": "Chest",
                "sort_order": 1,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            201,
        )

        self.assertTrue(
            WorkoutDay.objects.filter(
                workout_template=self.template,
                day_name="MONDAY",
            ).exists()
        )

    # =====================================================
    # WORKOUT EXERCISE API
    # =====================================================

    def test_employee_with_view_permission_can_list_template_exercises(self):
        self.role.permissions.add(
            self.view_permission
        )

        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.get(
            "/api/v1/workouts/template-exercises/"
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_employee_without_view_permission_cannot_list_template_exercises(self):
        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.get(
            "/api/v1/workouts/template-exercises/"
        )

        self.assertEqual(
            response.status_code,
            403,
        )

    def test_employee_with_create_permission_can_create_template_exercise(self):
        self.role.permissions.add(
            self.create_permission
        )

        day = WorkoutDay.objects.create(
            workout_template=self.template,
            day_name="MONDAY",
            focus_area="Chest",
            sort_order=1,
        )

        muscle_group = MuscleGroup.objects.create(
            name="Chest",
        )

        category = ExerciseCategory.objects.create(
            name="Push",
        )

        equipment = Equipment.objects.create(
            name="Barbell",
        )

        exercise = Exercise.objects.create(
            name="API Bench Press",
            muscle_group=muscle_group,
            category=category,
            equipment=equipment,
            difficulty="INTERMEDIATE",
            instructions="Press the bar upward.",
        )

        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.post(
            "/api/v1/workouts/template-exercises/",
            {
                "workout_day": day.id,
                "exercise": exercise.id,
                "exercise_order": 1,
                "sets": 4,
                "reps": "8-10",
                "rest_seconds": 90,
                "tempo": "3-1-1",
                "rpe": 8,
                "notes": "Controlled movement.",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            201,
        )

        self.assertTrue(
            WorkoutExercise.objects.filter(
                workout_day=day,
                exercise=exercise,
            ).exists()
        )