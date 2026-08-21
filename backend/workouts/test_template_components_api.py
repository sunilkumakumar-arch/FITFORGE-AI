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
    Exercise,
    MuscleGroup,
    ExerciseCategory,
)


User = get_user_model()


class WorkoutTemplateComponentsAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            username="template_components_api_user",
            password="TestPassword123!",
        )

        self.organization = Organization.objects.create(
            name="Template Components API Organization",
            owner_name="Test Owner",
            email="template.components@example.com",
            phone="9999999999",
        )

        self.branch = Branch.objects.create(
            organization=self.organization,
            name="Template Components API Branch",
            city="Hyderabad",
            address="Test Address",
        )

        self.view_permission = Permission.objects.create(
            module="workout",
            code="workout.view",
            name="View Workout Components",
            is_active=True,
        )

        self.create_permission = Permission.objects.create(
            module="workout",
            code="workout.create",
            name="Create Workout Components",
            is_active=True,
        )

        self.update_permission = Permission.objects.create(
            module="workout",
            code="workout.update",
            name="Update Workout Components",
            is_active=True,
        )

        self.delete_permission = Permission.objects.create(
            module="workout",
            code="workout.delete",
            name="Delete Workout Components",
            is_active=True,
        )

        self.role = Role.objects.create(
            code="TEST_TEMPLATE_COMPONENTS_API",
            name="Test Template Components API Role",
            is_active=True,
        )

        self.employee = Employee.objects.create(
            employee_code="TESTTEMPLATECOMP001",
            user=self.user,
            first_name="Template",
            last_name="API Tester",
            email="template.components.employee@example.com",
            phone="9999999998",
            organization=self.organization,
            branch=self.branch,
            joining_date=date.today(),
            employment_status="ACTIVE",
            role=self.role,
        )

        self.muscle_group = MuscleGroup.objects.create(
            name="Template Chest",
            description="Chest muscle group",
            display_order=1,
            is_active=True,
        )

        self.category = ExerciseCategory.objects.create(
            name="Template Push",
            description="Push category",
            is_active=True,
        )

        self.exercise = Exercise.objects.create(
            name="Template Bench Press",
            muscle_group=self.muscle_group,
            category=self.category,
            difficulty="INTERMEDIATE",
            instructions="Press the bar upward.",
            description="Template exercise.",
            primary_muscles="Chest",
            secondary_muscles="Triceps",
            calories_factor="1.20",
            is_active=True,
        )

        self.template = WorkoutTemplate.objects.create(
            name="API Test Workout Template",
            description="Template API test.",
            goal="MUSCLE_GAIN",
            difficulty="INTERMEDIATE",
            duration_weeks=8,
            is_active=True,
        )

        self.day = WorkoutDay.objects.create(
            workout_template=self.template,
            day_name="MONDAY",
            focus_area="Chest",
            sort_order=1,
        )

        self.workout_exercise = WorkoutExercise.objects.create(
            workout_day=self.day,
            exercise=self.exercise,
            exercise_order=1,
            sets=4,
            reps="8-12",
            rest_seconds=90,
            tempo="3-1-1",
            rpe=8,
            notes="Controlled reps.",
        )

    # =====================================================
    # Workout Template API
    # =====================================================

    def test_unauthenticated_user_cannot_list_templates(self):
        response = self.client.get(
            "/api/v1/workouts/templates/"
        )

        self.assertIn(
            response.status_code,
            [401, 403],
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

    def test_employee_with_view_permission_can_retrieve_template_with_nested_data(
        self,
    ):
        self.role.permissions.add(
            self.view_permission
        )

        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.get(
            f"/api/v1/workouts/templates/{self.template.id}/"
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertEqual(
            response.data["name"],
            "API Test Workout Template",
        )

        self.assertEqual(
            len(response.data["days"]),
            1,
        )

        self.assertEqual(
            response.data["days"][0]["day_name"],
            "MONDAY",
        )

        self.assertEqual(
            len(response.data["days"][0]["exercises"]),
            1,
        )

        self.assertEqual(
            response.data["days"][0]["exercises"][0][
                "exercise_name"
            ],
            "Template Bench Press",
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
                "name": "New API Workout Template",
                "description": "Created through API.",
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
                name="New API Workout Template"
            ).exists()
        )

    # =====================================================
    # Workout Day API
    # =====================================================

    def test_employee_with_view_permission_can_list_days(self):
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

    def test_employee_with_create_permission_can_create_day(self):
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
                "day_name": "WEDNESDAY",
                "focus_area": "Back",
                "sort_order": 2,
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
                day_name="WEDNESDAY",
            ).exists()
        )

    def test_employee_with_update_permission_can_update_day(self):
        self.role.permissions.add(
            self.update_permission
        )

        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.patch(
            f"/api/v1/workouts/days/{self.day.id}/",
            {
                "focus_area": "Upper Chest",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.day.refresh_from_db()

        self.assertEqual(
            self.day.focus_area,
            "Upper Chest",
        )

    def test_employee_with_delete_permission_can_delete_day(self):
        self.role.permissions.add(
            self.delete_permission
        )

        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.delete(
            f"/api/v1/workouts/days/{self.day.id}/"
        )

        self.assertEqual(
            response.status_code,
            204,
        )

        self.assertFalse(
            WorkoutDay.objects.filter(
                id=self.day.id
            ).exists()
        )

    # =====================================================
    # Workout Template Exercise API
    # =====================================================

    def test_employee_with_view_permission_can_list_template_exercises(
        self,
    ):
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

    def test_employee_with_create_permission_can_create_template_exercise(
        self,
    ):
        self.role.permissions.add(
            self.create_permission
        )

        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.post(
            "/api/v1/workouts/template-exercises/",
            {
                "workout_day": self.day.id,
                "exercise": self.exercise.id,
                "exercise_order": 2,
                "sets": 3,
                "reps": "10-12",
                "rest_seconds": 60,
                "tempo": "2-1-2",
                "rpe": 7,
                "notes": "API-created exercise.",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            201,
        )

        self.assertTrue(
            WorkoutExercise.objects.filter(
                workout_day=self.day,
                exercise_order=2,
            ).exists()
        )

    def test_template_exercise_returns_exercise_name(self):
        self.role.permissions.add(
            self.view_permission
        )

        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.get(
            f"/api/v1/workouts/template-exercises/"
            f"{self.workout_exercise.id}/"
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertEqual(
            response.data["exercise_name"],
            "Template Bench Press",
        )

    def test_employee_with_update_permission_can_update_template_exercise(
        self,
    ):
        self.role.permissions.add(
            self.update_permission
        )

        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.patch(
            f"/api/v1/workouts/template-exercises/"
            f"{self.workout_exercise.id}/",
            {
                "sets": 5,
                "rest_seconds": 120,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.workout_exercise.refresh_from_db()

        self.assertEqual(
            self.workout_exercise.sets,
            5,
        )

        self.assertEqual(
            self.workout_exercise.rest_seconds,
            120,
        )

    def test_employee_with_delete_permission_can_delete_template_exercise(
        self,
    ):
        self.role.permissions.add(
            self.delete_permission
        )

        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.delete(
            f"/api/v1/workouts/template-exercises/"
            f"{self.workout_exercise.id}/"
        )

        self.assertEqual(
            response.status_code,
            204,
        )

        self.assertFalse(
            WorkoutExercise.objects.filter(
                id=self.workout_exercise.id
            ).exists()
        )