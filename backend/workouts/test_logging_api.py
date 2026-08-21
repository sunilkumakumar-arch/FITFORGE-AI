from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from accounts.models import Member
from core.models import Organization, Branch
from employees.models import Employee
from roles.models import Role, Permission
from trainers.models import Trainer

from workouts.models import (
    MuscleGroup,
    ExerciseCategory,
    Exercise,
    WorkoutTemplate,
    WorkoutDay,
    WorkoutExercise,
    MemberWorkoutPlan,
    MemberWorkoutDay,
    WorkoutLog,
    ExerciseLog,
)

from workouts.services.assignment_service import AssignmentService


User = get_user_model()


class WorkoutLoggingAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()

        # =====================================================
        # USER
        # =====================================================

        self.user = User.objects.create_user(
            username="workout_logging_api_user",
            password="TestPassword123!",
        )

        # =====================================================
        # ORGANIZATION
        # =====================================================

        self.organization = Organization.objects.create(
            name="Workout Logging API Organization",
            owner_name="Test Owner",
            email="workout.logging@example.com",
            phone="9999999001",
        )

        self.branch = Branch.objects.create(
            organization=self.organization,
            name="Workout Logging Branch",
            city="Hyderabad",
            address="Test Address",
        )

        # =====================================================
        # PERMISSIONS
        # =====================================================

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

        # =====================================================
        # ROLE
        # =====================================================

        self.role = Role.objects.create(
            code="TEST_WORKOUT_LOGGING_API",
            name="Test Workout Logging API Role",
            is_active=True,
        )

        # =====================================================
        # EMPLOYEE
        # =====================================================

        self.employee = Employee.objects.create(
            employee_code="TESTWORKOUTLOG001",
            user=self.user,
            first_name="Workout",
            last_name="Logging Tester",
            email="workout.logging.employee@example.com",
            phone="9999999002",
            organization=self.organization,
            branch=self.branch,
            joining_date=date.today(),
            employment_status="ACTIVE",
            role=self.role,
        )

        # =====================================================
        # MEMBER
        # =====================================================

        self.member = Member.objects.create(
            first_name="Workout",
            last_name="Member",
            phone="9999999003",
            email="workout.logging.member@example.com",
            gender="Male",
            date_of_birth=date(1995, 1, 1),
        )

        # =====================================================
        # TRAINER
        # =====================================================

        self.trainer = Trainer.objects.create(
            first_name="Test",
            last_name="Trainer",
            phone="9999999004",
            email="workout.logging.trainer@example.com",
            employment_status="Active",
        )

        # =====================================================
        # EXERCISE MASTER DATA
        # =====================================================

        self.muscle_group = MuscleGroup.objects.create(
            name="Chest",
            description="Chest muscle group",
            display_order=1,
            is_active=True,
        )

        self.exercise_category = ExerciseCategory.objects.create(
            name="Push",
            description="Push exercises",
            is_active=True,
        )

        self.exercise = Exercise.objects.create(
            name="Bench Press",
            muscle_group=self.muscle_group,
            category=self.exercise_category,
            difficulty="INTERMEDIATE",
            instructions="Press the bar upward from the chest.",
            description="Barbell bench press.",
            primary_muscles="Chest",
            secondary_muscles="Triceps, Shoulders",
            calories_factor=1.00,
            is_active=True,
        )

        # =====================================================
        # WORKOUT TEMPLATE
        # =====================================================

        self.template = WorkoutTemplate.objects.create(
            name="API Logging Test Template",
            description="Workout logging API test template.",
            goal="MUSCLE_GAIN",
            difficulty="INTERMEDIATE",
            duration_weeks=8,
            created_by=self.trainer,
            is_active=True,
        )

        self.workout_day = WorkoutDay.objects.create(
            workout_template=self.template,
            day_name="MONDAY",
            focus_area="Chest",
            sort_order=1,
        )

        self.workout_exercise = WorkoutExercise.objects.create(
            workout_day=self.workout_day,
            exercise=self.exercise,
            exercise_order=1,
            sets=4,
            reps="8-12",
            rest_seconds=90,
            tempo="2-0-2",
            rpe=8,
            notes="Controlled movement.",
        )

        # =====================================================
        # ASSIGN WORKOUT TO MEMBER
        # =====================================================

        self.member_plan = AssignmentService.assign_template(
            member=self.member,
            workout_template=self.template,
            trainer=self.trainer,
            assigned_by=self.user,
        )

        self.member_workout_day = MemberWorkoutDay.objects.get(
            member_workout=self.member_plan,
            workout_day=self.workout_day,
        )

    # =========================================================
    # AUTHENTICATION
    # =========================================================

    def test_unauthenticated_user_cannot_list_workout_logs(self):
        response = self.client.get(
            "/api/v1/workouts/logs/"
        )

        self.assertIn(
            response.status_code,
            [401, 403],
        )

    # =========================================================
    # VIEW PERMISSION
    # =========================================================

    def test_employee_with_view_permission_can_list_workout_logs(self):
        self.role.permissions.add(
            self.view_permission
        )

        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.get(
            "/api/v1/workouts/logs/"
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_employee_without_view_permission_cannot_list_workout_logs(self):
        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.get(
            "/api/v1/workouts/logs/"
        )

        self.assertEqual(
            response.status_code,
            403,
        )

    # =========================================================
    # START WORKOUT
    # =========================================================

    def test_employee_with_create_permission_can_start_workout(self):
        self.role.permissions.add(
            self.create_permission
        )

        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.post(
            "/api/v1/workouts/logs/",
            {
                "workout_day": self.member_workout_day.id,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            201,
        )

        workout_log = WorkoutLog.objects.get(
            workout_day=self.member_workout_day,
        )

        self.assertEqual(
            workout_log.member_workout,
            self.member_plan,
        )

        self.assertEqual(
            workout_log.status,
            "PARTIAL",
        )

    # =========================================================
    # LOG EXERCISE
    # =========================================================

    def test_employee_with_update_permission_can_log_exercise(self):
        self.role.permissions.add(
            self.update_permission
        )

        workout_log = WorkoutLog.objects.create(
            member_workout=self.member_plan,
            workout_day=self.member_workout_day,
            workout_date=date.today(),
            status="PARTIAL",
        )

        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.post(
            f"/api/v1/workouts/logs/{workout_log.id}/exercises/",
            {
                "workout_exercise": self.workout_exercise.id,
                "sets_completed": 4,
                "reps_completed": "10",
                "weight_used": "80.00",
                "rpe": 8,
                "notes": "Good performance.",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            201,
        )

        exercise_log = ExerciseLog.objects.get(
            workout_log=workout_log,
            workout_exercise=self.workout_exercise,
        )

        self.assertEqual(
            exercise_log.sets_completed,
            4,
        )

        self.assertEqual(
            exercise_log.reps_completed,
            "10",
        )

        self.assertEqual(
            exercise_log.weight_used,
            80,
        )

        self.assertEqual(
            exercise_log.rpe,
            8,
        )

    # =========================================================
    # EXERCISE HISTORY
    # =========================================================

    def test_employee_with_view_permission_can_get_exercise_history(self):
        self.role.permissions.add(
            self.view_permission
        )

        workout_log = WorkoutLog.objects.create(
            member_workout=self.member_plan,
            workout_day=self.member_workout_day,
            workout_date=date.today(),
            status="PARTIAL",
        )

        ExerciseLog.objects.create(
            workout_log=workout_log,
            workout_exercise=self.workout_exercise,
            completed=True,
            sets_completed=4,
            reps_completed="10",
            weight_used=80,
            rpe=8,
            rest_seconds=90,
            notes="Good session.",
        )

        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.get(
            "/api/v1/workouts/logs/exercise-history/",
            {
                "member": self.member.id,
                "exercise": self.exercise.id,
            },
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

        self.assertEqual(
            response.data[0]["exercise_name"],
            "Bench Press",
        )

    # =========================================================
    # EXERCISE HISTORY VALIDATION
    # =========================================================

    def test_exercise_history_requires_member(self):
        self.role.permissions.add(
            self.view_permission
        )

        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.get(
            "/api/v1/workouts/logs/exercise-history/",
            {
                "exercise": self.exercise.id,
            },
        )

        self.assertEqual(
            response.status_code,
            400,
        )

    def test_exercise_history_requires_exercise(self):
        self.role.permissions.add(
            self.view_permission
        )

        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.get(
            "/api/v1/workouts/logs/exercise-history/",
            {
                "member": self.member.id,
            },
        )

        self.assertEqual(
            response.status_code,
            400,
        )

    # =========================================================
    # FINISH WORKOUT
    # =========================================================

    def test_employee_with_update_permission_can_finish_workout(self):
        self.role.permissions.add(
            self.update_permission
        )

        workout_log = WorkoutLog.objects.create(
            member_workout=self.member_plan,
            workout_day=self.member_workout_day,
            workout_date=date.today(),
            status="PARTIAL",
        )

        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.post(
            f"/api/v1/workouts/logs/{workout_log.id}/finish/",
            {
                "duration_minutes": 60,
                "calories_burned": 450,
                "notes": "Completed successfully.",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        workout_log.refresh_from_db()
        self.member_workout_day.refresh_from_db()

        self.assertEqual(
            workout_log.status,
            "COMPLETED",
        )

        self.assertEqual(
            workout_log.duration_minutes,
            60,
        )

        self.assertEqual(
            workout_log.calories_burned,
            450,
        )

        self.assertTrue(
            self.member_workout_day.completed
        )

        self.assertIsNotNone(
            self.member_workout_day.completed_at
        )
        