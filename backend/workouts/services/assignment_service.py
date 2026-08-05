from django.db import transaction
from rest_framework.exceptions import ValidationError

from workouts.models import (
    WorkoutTemplate,
    WorkoutDay,
    WorkoutExercise,
    MemberWorkoutPlan,
    MemberWorkoutDay,
)


class WorkoutAssignmentService:
    """
    Business logic for assigning workout plans.
    """

    @staticmethod
    @transaction.atomic
    def assign_template(
        *,
        member,
        workout_template,
        trainer=None,
        assigned_by=None,
        assignment_type="GENERAL",
        source="TEMPLATE",
        start_date,
        notes="",
    ):
        """
        Assign a workout template to a member.
        """

        active_plan = (
            MemberWorkoutPlan.objects
            .filter(
                member=member,
                status="ACTIVE",
            )
            .first()
        )

        if active_plan:
            raise ValidationError(
                {
                    "member":
                    "Member already has an active workout plan."
                }
            )

        member_plan = MemberWorkoutPlan.objects.create(
            member=member,
            workout_template=workout_template,
            trainer=trainer,
            assigned_by=assigned_by,
            last_updated_by=assigned_by,
            assignment_type=assignment_type,
            source=source,
            version=1,
            start_date=start_date,
            status="ACTIVE",
            notes=notes,
        )

        days = (
            WorkoutDay.objects
            .filter(
                workout_template=workout_template
            )
            .order_by("sort_order")
        )

        for day in days:

            MemberWorkoutDay.objects.create(
                member_workout=member_plan,
                workout_day=day,
            )

        return member_plan