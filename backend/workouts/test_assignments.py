from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.exceptions import ValidationError

from accounts.models import Member
from trainers.models import Trainer
from workouts.models import (
    WorkoutTemplate,
    WorkoutDay,
    MemberWorkoutPlan,
    MemberWorkoutDay,
)
from workouts.services.assignment_service import AssignmentService


User = get_user_model()


class WorkoutAssignmentServiceTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="workout_assignment_user",
            password="TestPassword123!",
        )

        self.member = Member.objects.create(
            first_name="Workout",
            last_name="Member",
            phone="9999991001",
            email="workout.member@example.com",
            gender="Male",
            date_of_birth=date(1995, 1, 1),
        )

        self.trainer = Trainer.objects.create(
            first_name="Test",
            last_name="Trainer",
            phone="9999999999",
            email="trainer.test@example.com",
            employment_status="Active",
        )

        self.template = WorkoutTemplate.objects.create(
            name="Assignment Test Template",
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

        self.day3 = WorkoutDay.objects.create(
            workout_template=self.template,
            day_name="FRIDAY",
            focus_area="Legs",
            sort_order=3,
        )

    def test_assign_template_creates_member_workout_plan(self):
        plan = AssignmentService.assign_template(
            member=self.member,
            workout_template=self.template,
            trainer=self.trainer,
            assigned_by=self.user,
        )

        self.assertIsNotNone(plan.id)
        self.assertEqual(plan.member, self.member)
        self.assertEqual(plan.workout_template, self.template)
        self.assertEqual(plan.trainer, self.trainer)
        self.assertEqual(plan.assigned_by, self.user)
        self.assertEqual(plan.last_updated_by, self.user)
        self.assertEqual(plan.status, "ACTIVE")
        self.assertEqual(plan.version, 1)

    def test_assign_template_creates_member_workout_days(self):
        plan = AssignmentService.assign_template(
            member=self.member,
            workout_template=self.template,
            trainer=self.trainer,
            assigned_by=self.user,
        )

        days = MemberWorkoutDay.objects.filter(
            member_workout=plan
        ).order_by("workout_day__sort_order")

        self.assertEqual(days.count(), 3)

        self.assertEqual(
            list(
                days.values_list(
                    "workout_day__day_name",
                    flat=True,
                )
            ),
            [
                "MONDAY",
                "WEDNESDAY",
                "FRIDAY",
            ],
        )

    def test_assign_template_rejects_existing_active_plan(self):
        AssignmentService.assign_template(
            member=self.member,
            workout_template=self.template,
            trainer=self.trainer,
            assigned_by=self.user,
        )

        with self.assertRaises(ValidationError):
            AssignmentService.assign_template(
                member=self.member,
                workout_template=self.template,
                trainer=self.trainer,
                assigned_by=self.user,
            )

    def test_complete_plan_changes_status_and_end_date(self):
        plan = AssignmentService.assign_template(
            member=self.member,
            workout_template=self.template,
            trainer=self.trainer,
            assigned_by=self.user,
        )

        completed_plan = AssignmentService.complete_plan(
            member_plan=plan
        )

        self.assertEqual(
            completed_plan.status,
            "COMPLETED",
        )

        self.assertEqual(
            completed_plan.end_date,
            date.today(),
        )

    def test_complete_plan_rejects_non_active_plan(self):
        plan = AssignmentService.assign_template(
            member=self.member,
            workout_template=self.template,
            trainer=self.trainer,
            assigned_by=self.user,
        )

        AssignmentService.complete_plan(
            member_plan=plan
        )

        with self.assertRaises(ValidationError):
            AssignmentService.complete_plan(
                member_plan=plan
            )

    def test_cancel_plan_changes_status_and_end_date(self):
        plan = AssignmentService.assign_template(
            member=self.member,
            workout_template=self.template,
            trainer=self.trainer,
            assigned_by=self.user,
        )

        cancelled_plan = AssignmentService.cancel_plan(
            member_plan=plan
        )

        self.assertEqual(
            cancelled_plan.status,
            "CANCELLED",
        )

        self.assertEqual(
            cancelled_plan.end_date,
            date.today(),
        )

    def test_cancel_plan_rejects_non_active_plan(self):
        plan = AssignmentService.assign_template(
            member=self.member,
            workout_template=self.template,
            trainer=self.trainer,
            assigned_by=self.user,
        )

        AssignmentService.cancel_plan(
            member_plan=plan
        )

        with self.assertRaises(ValidationError):
            AssignmentService.cancel_plan(
                member_plan=plan
            )

    def test_change_template_replaces_member_days_and_increments_version(self):
        plan = AssignmentService.assign_template(
            member=self.member,
            workout_template=self.template,
            trainer=self.trainer,
            assigned_by=self.user,
        )

        new_template = WorkoutTemplate.objects.create(
            name="Replacement Template",
            goal="STRENGTH",
            difficulty="ADVANCED",
            duration_weeks=6,
            created_by=self.trainer,
        )

        new_day1 = WorkoutDay.objects.create(
            workout_template=new_template,
            day_name="TUESDAY",
            focus_area="Shoulders",
            sort_order=1,
        )

        new_day2 = WorkoutDay.objects.create(
            workout_template=new_template,
            day_name="THURSDAY",
            focus_area="Arms",
            sort_order=2,
        )

        updated_plan = AssignmentService.change_template(
            member_plan=plan,
            workout_template=new_template,
            updated_by=self.user,
        )

        self.assertEqual(
            updated_plan.workout_template,
            new_template,
        )

        self.assertEqual(
            updated_plan.version,
            2,
        )

        self.assertEqual(
            updated_plan.last_updated_by,
            self.user,
        )

        days = MemberWorkoutDay.objects.filter(
            member_workout=updated_plan
        ).order_by("workout_day__sort_order")

        self.assertEqual(days.count(), 2)

        self.assertEqual(
            list(
                days.values_list(
                    "workout_day__day_name",
                    flat=True,
                )
            ),
            [
                "TUESDAY",
                "THURSDAY",
            ],
        )

        self.assertFalse(
            days.filter(
                workout_day__workout_template=self.template
            ).exists()
        )

    def test_change_template_rejects_non_active_plan(self):
        plan = AssignmentService.assign_template(
            member=self.member,
            workout_template=self.template,
            trainer=self.trainer,
            assigned_by=self.user,
        )

        AssignmentService.complete_plan(
            member_plan=plan
        )

        new_template = WorkoutTemplate.objects.create(
            name="Inactive Change Template",
            goal="GENERAL_FITNESS",
            difficulty="BEGINNER",
            duration_weeks=4,
            created_by=self.trainer,
        )

        with self.assertRaises(ValidationError):
            AssignmentService.change_template(
                member_plan=plan,
                workout_template=new_template,
                updated_by=self.user,
            )
