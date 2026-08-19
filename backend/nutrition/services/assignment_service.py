from django.db import transaction
from rest_framework.exceptions import ValidationError

from nutrition.models import MemberNutritionAssignment


class NutritionAssignmentService:
    """
    Business logic for assigning nutrition plans to members.
    """

    @staticmethod
    @transaction.atomic
    def assign_plan(
        *,
        member,
        nutrition_plan,
        assigned_by=None,
        assigned_by_employee=None,
    ):
        """
        Assign a nutrition plan to a member.

        Business rule:
        A member can have only one active nutrition
        assignment at a time.

        If an active assignment already exists,
        it will be deactivated before the new plan
        is assigned.

        Audit:
        - assigned_by is used when a Trainer performs
          the assignment.
        - assigned_by_employee is used when an Employee
          such as a Branch Manager performs the assignment.
        """

        if not nutrition_plan:
            raise ValidationError(
                {
                    "nutrition_plan": (
                        "Nutrition plan is required."
                    )
                }
            )

        if assigned_by is not None and assigned_by_employee is not None:
            raise ValidationError(
                {
                    "assigned_by": (
                        "Only one assignment actor can be provided."
                    )
                }
            )

        existing_assignment = (
            MemberNutritionAssignment.objects
            .select_for_update()
            .filter(
                member=member,
                active=True,
            )
            .first()
        )

        if existing_assignment:
            existing_assignment.active = False
            existing_assignment.save(
                update_fields=["active"]
            )

        assignment = (
            MemberNutritionAssignment.objects.create(
                member=member,
                nutrition_plan=nutrition_plan,
                assigned_by=assigned_by,
                assigned_by_employee=assigned_by_employee,
                active=True,
            )
        )

        return assignment

    @staticmethod
    @transaction.atomic
    def deactivate_assignment(
        *,
        assignment,
    ):
        """
        Deactivate a nutrition assignment.
        """

        if not assignment.active:
            return assignment

        assignment.active = False

        assignment.save(
            update_fields=["active"]
        )

        return assignment