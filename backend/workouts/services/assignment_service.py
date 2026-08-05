from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from workouts.models import (
    MemberWorkoutPlan,
    MemberWorkoutDay,
)

from workouts.selectors.assignment_selector import AssignmentSelector


class AssignmentService:

    @staticmethod
    @transaction.atomic
    def assign_template(
        *,
        member,
        workout_template,
        trainer,
        assigned_by,
        assignment_type="GENERAL",
        source="TEMPLATE",
        start_date=None,
        notes="",
    ):
        """
        Assign a workout template to a member.
        Automatically creates MemberWorkoutDay records.
        """

        active_plan = AssignmentSelector.get_active_plan(member)

        if active_plan:
            raise ValidationError(
                {
                    "member": "Member already has an active workout plan."
                }
            )

        if start_date is None:
            start_date = timezone.now().date()

        member_plan = MemberWorkoutPlan.objects.create(
            member=member,
            workout_template=workout_template,
            trainer=trainer,
            assigned_by=assigned_by,
            last_updated_by=assigned_by,
            assignment_type=assignment_type,
            source=source,
            start_date=start_date,
            status="ACTIVE",
            notes=notes,
        )

        for day in workout_template.days.all().order_by("sort_order"):

            MemberWorkoutDay.objects.create(
                member_workout=member_plan,
                workout_day=day,
            )

        return member_plan


    @staticmethod
    @transaction.atomic
    def complete_plan(*, member_plan):

        if member_plan.status != "ACTIVE":
            raise ValidationError(
                {
                    "plan": "Only active workout plans can be completed."
                }
            )

        member_plan.status = "COMPLETED"
        member_plan.end_date = timezone.now().date()

        member_plan.save(
            update_fields=[
                "status",
                "end_date",
                "updated_at",
            ]
        )

        return member_plan

    @staticmethod
    @transaction.atomic
    def cancel_plan(*, member_plan):

        if member_plan.status != "ACTIVE":
            raise ValidationError(
                {
                    "plan": "Only active workout plans can be cancelled."
                }
            )

        member_plan.status = "CANCELLED"
        member_plan.end_date = timezone.now().date()

        member_plan.save(
            update_fields=[
                "status",
                "end_date",
                "updated_at",
            ]
        )

        return member_plan

    @staticmethod
    @transaction.atomic
    def change_template(
        *,
        member_plan,
        workout_template,
        updated_by,
    ):

        if member_plan.status != "ACTIVE":
            raise ValidationError(
                {
                    "plan": "Only active workout plans can be modified."
                }
            )

        MemberWorkoutDay.objects.filter(
            member_workout=member_plan
        ).delete()

        member_plan.workout_template = workout_template
        member_plan.version += 1
        member_plan.last_updated_by = updated_by

        member_plan.save(
            update_fields=[
                "workout_template",
                "version",
                "last_updated_by",
                "updated_at",
            ]
        )

        for day in workout_template.days.all().order_by("sort_order"):

            MemberWorkoutDay.objects.create(
                member_workout=member_plan,
                workout_day=day,
            )

        return member_plan    