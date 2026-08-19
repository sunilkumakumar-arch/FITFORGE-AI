from rest_framework import status, viewsets
from rest_framework.response import Response
from roles.permissions import RolePermission

from employees.models import Employee

from .models import (
    NutritionPlan,
    Meal,
    MemberNutritionAssignment,
)

from .serializers import (
    NutritionPlanSerializer,
    MealSerializer,
    MemberNutritionAssignmentSerializer,
)

from .services.assignment_service import (
    NutritionAssignmentService,
)


class NutritionPlanViewSet(viewsets.ModelViewSet):

    queryset = NutritionPlan.objects.all()

    serializer_class = NutritionPlanSerializer

    permission_classes = [RolePermission]

    permission_map = {
        "list": "nutrition.view",
        "retrieve": "nutrition.view",
        "create": "nutrition.create",
        "update": "nutrition.update",
        "partial_update": "nutrition.update",
        "destroy": "nutrition.delete",
    }


class MealViewSet(viewsets.ModelViewSet):

    queryset = Meal.objects.all()

    serializer_class = MealSerializer

    permission_classes = [RolePermission]

    permission_map = {
        "list": "nutrition.view",
        "retrieve": "nutrition.view",
        "create": "nutrition.create",
        "update": "nutrition.update",
        "partial_update": "nutrition.update",
        "destroy": "nutrition.delete",
    }


class MemberNutritionAssignmentViewSet(viewsets.ModelViewSet):

    queryset = (
        MemberNutritionAssignment.objects
        .select_related(
            "member",
            "nutrition_plan",
            "assigned_by",
            "assigned_by_employee",
        )
        .order_by("-id")
    )

    serializer_class = MemberNutritionAssignmentSerializer

    permission_classes = [RolePermission]

    permission_map = {
        "list": "nutrition.view",
        "retrieve": "nutrition.view",
        "create": "nutrition.assign",
        "update": "nutrition.update",
        "partial_update": "nutrition.update",
        "destroy": "nutrition.delete",
    }

    def create(self, request, *args, **kwargs):
        """
        Assign a nutrition plan to a member.

        The assignment is created through the service layer
        so that nutrition business rules cannot be bypassed.

        The authenticated Employee is recorded as the actor
        when the request is made by an employee such as a
        Branch Manager.
        """

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        member = serializer.validated_data["member"]

        nutrition_plan = serializer.validated_data[
            "nutrition_plan"
        ]

        employee = Employee.objects.filter(
            user=request.user,
            employment_status="ACTIVE",
        ).first()

        if employee is None:
            return Response(
                {
                    "success": False,
                    "message": "Active employee profile not found.",
                    "errors": {
                        "employee": (
                            "The authenticated user is not linked "
                            "to an active employee."
                        )
                    },
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        assignment = (
            NutritionAssignmentService.assign_plan(
                member=member,
                nutrition_plan=nutrition_plan,
                assigned_by_employee=employee,
            )
        )

        response_serializer = self.get_serializer(
            assignment
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )