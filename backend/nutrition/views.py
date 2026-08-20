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

from .services.meal_service import (
    NutritionMealService,
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

    queryset = (
        Meal.objects
        .select_related(
            "nutrition_plan",
        )
        .order_by(
            "nutrition_plan_id",
            "id",
        )
    )

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

    def create(self, request, *args, **kwargs):
        """
        Create a meal under a nutrition plan.

        Meal creation is routed through the service layer
        so nutrition business rules cannot be bypassed.
        """

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        meal = NutritionMealService.create_meal(
            nutrition_plan=serializer.validated_data[
                "nutrition_plan"
            ],
            meal_name=serializer.validated_data[
                "meal_name"
            ],
            meal_time=serializer.validated_data[
                "meal_time"
            ],
            foods=serializer.validated_data[
                "foods"
            ],
            calories=serializer.validated_data[
                "calories"
            ],
        )

        response_serializer = self.get_serializer(
            meal
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        """
        Update a meal through the service layer.
        """

        partial = kwargs.pop(
            "partial",
            False,
        )

        meal = self.get_object()

        serializer = self.get_serializer(
            meal,
            data=request.data,
            partial=partial,
        )

        serializer.is_valid(
            raise_exception=True
        )

        updated_meal = NutritionMealService.update_meal(
            meal=meal,
            meal_name=serializer.validated_data.get(
                "meal_name"
            ),
            meal_time=serializer.validated_data.get(
                "meal_time"
            ),
            foods=serializer.validated_data.get(
                "foods"
            ),
            calories=serializer.validated_data.get(
                "calories"
            ),
        )

        response_serializer = self.get_serializer(
            updated_meal
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_200_OK,
        )

    def partial_update(
        self,
        request,
        *args,
        **kwargs,
    ):
        """
        Partial update of a meal through the service layer.
        """

        kwargs["partial"] = True

        return self.update(
            request,
            *args,
            **kwargs,
        )


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