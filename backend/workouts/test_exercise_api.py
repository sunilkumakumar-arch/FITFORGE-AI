from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from core.models import Organization, Branch
from employees.models import Employee
from roles.models import Role, Permission
from workouts.models import (
    Exercise,
    MuscleGroup,
    ExerciseCategory,
    Equipment,
)


User = get_user_model()


class ExerciseAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            username="exercise_api_user",
            password="TestPassword123!",
        )

        self.organization = Organization.objects.create(
            name="Exercise API Organization",
            owner_name="Test Owner",
            email="exercise.api@example.com",
            phone="9999999999",
        )

        self.branch = Branch.objects.create(
            organization=self.organization,
            name="Exercise API Branch",
            city="Hyderabad",
            address="Test Address",
        )

        self.view_permission = Permission.objects.create(
            module="workout",
            code="workout.view",
            name="View Workout",
            is_active=True,
        )

        self.create_permission = Permission.objects.create(
            module="workout",
            code="workout.create",
            name="Create Workout",
            is_active=True,
        )

        self.update_permission = Permission.objects.create(
            module="workout",
            code="workout.update",
            name="Update Workout",
            is_active=True,
        )

        self.delete_permission = Permission.objects.create(
            module="workout",
            code="workout.delete",
            name="Delete Workout",
            is_active=True,
        )

        self.role = Role.objects.create(
            code="TEST_EXERCISE_API",
            name="Test Exercise API Role",
            is_active=True,
        )

        self.employee = Employee.objects.create(
            employee_code="TESTEXERCISE001",
            user=self.user,
            first_name="Exercise",
            last_name="API Tester",
            email="exercise.api.employee@example.com",
            phone="9999999998",
            organization=self.organization,
            branch=self.branch,
            joining_date=date.today(),
            employment_status="ACTIVE",
            role=self.role,
        )

        self.muscle_group = MuscleGroup.objects.create(
            name="Chest",
            description="Chest muscle group",
            display_order=1,
            is_active=True,
        )

        self.category = ExerciseCategory.objects.create(
            name="Push",
            description="Push exercises",
            is_active=True,
        )

        self.equipment = Equipment.objects.create(
            name="Barbell",
            description="Olympic barbell",
            is_active=True,
        )

        self.exercise = Exercise.objects.create(
            name="Barbell Bench Press",
            muscle_group=self.muscle_group,
            category=self.category,
            equipment=self.equipment,
            difficulty="INTERMEDIATE",
            instructions="Press the barbell upward from the chest.",
            description="Compound chest pressing exercise.",
            primary_muscles="Chest",
            secondary_muscles="Triceps, Shoulders",
            calories_factor=1.50,
            is_active=True,
        )

    def test_unauthenticated_user_cannot_list_exercises(self):
        response = self.client.get(
            "/api/v1/workouts/exercises/"
        )

        self.assertIn(
            response.status_code,
            [401, 403],
        )

    def test_employee_with_view_permission_can_list_exercises(self):
        self.role.permissions.add(
            self.view_permission
        )

        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.get(
            "/api/v1/workouts/exercises/"
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_employee_without_view_permission_cannot_list_exercises(self):
        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.get(
            "/api/v1/workouts/exercises/"
        )

        self.assertEqual(
            response.status_code,
            403,
        )

    def test_employee_with_create_permission_can_create_exercise(self):
        self.role.permissions.add(
            self.create_permission
        )

        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.post(
            "/api/v1/workouts/exercises/",
            {
                "name": "Incline Dumbbell Press",
                "muscle_group": self.muscle_group.id,
                "category": self.category.id,
                "equipment": self.equipment.id,
                "difficulty": "INTERMEDIATE",
                "instructions": "Press dumbbells upward.",
                "description": "Upper chest pressing exercise.",
                "primary_muscles": "Chest",
                "secondary_muscles": "Triceps, Shoulders",
                "calories_factor": "1.30",
                "is_active": True,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            201,
        )

        self.assertTrue(
            Exercise.objects.filter(
                name="Incline Dumbbell Press"
            ).exists()
        )

    def test_employee_with_view_permission_can_retrieve_exercise(self):
        self.role.permissions.add(
            self.view_permission
        )

        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.get(
            f"/api/v1/workouts/exercises/{self.exercise.id}/"
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertEqual(
            response.data["name"],
            "Barbell Bench Press",
        )

        self.assertEqual(
            response.data["muscle_group_name"],
            "Chest",
        )

        self.assertEqual(
            response.data["category_name"],
            "Push",
        )

        self.assertEqual(
            response.data["equipment_name"],
            "Barbell",
        )

    def test_employee_with_update_permission_can_update_exercise(self):
        self.role.permissions.add(
            self.update_permission
        )

        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.patch(
            f"/api/v1/workouts/exercises/{self.exercise.id}/",
            {
                "name": "Barbell Bench Press Updated",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.exercise.refresh_from_db()

        self.assertEqual(
            self.exercise.name,
            "Barbell Bench Press Updated",
        )

    def test_employee_without_update_permission_cannot_update_exercise(self):
        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.patch(
            f"/api/v1/workouts/exercises/{self.exercise.id}/",
            {
                "name": "Unauthorized Update",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            403,
        )

    def test_employee_with_delete_permission_can_delete_exercise(self):
        self.role.permissions.add(
            self.delete_permission
        )

        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.delete(
            f"/api/v1/workouts/exercises/{self.exercise.id}/"
        )

        self.assertEqual(
            response.status_code,
            204,
        )

        self.assertFalse(
            Exercise.objects.filter(
                id=self.exercise.id
            ).exists()
        )

    def test_employee_without_delete_permission_cannot_delete_exercise(self):
        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.delete(
            f"/api/v1/workouts/exercises/{self.exercise.id}/"
        )

        self.assertEqual(
            response.status_code,
            403,
        )