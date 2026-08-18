from rest_framework import status, viewsets
from rest_framework.decorators import action
from roles.permissions import RolePermission
from rest_framework.response import Response

from workouts.models import MemberWorkoutPlan
from workouts.serializers import MemberWorkoutPlanSerializer
from workouts.services.assignment_service import AssignmentService


class MemberWorkoutPlanViewSet(viewsets.ModelViewSet):

    queryset = (
        MemberWorkoutPlan.objects
        .select_related(
            "member",
            "trainer",
            "workout_template",
        )
        .prefetch_related("days")
        .all()
    )

    serializer_class = MemberWorkoutPlanSerializer
    permission_classes = [RolePermission]

    permission_map = {
        "list": "workout.view",
        "retrieve": "workout.view",
        "create": "workout.create",
        "update": "workout.update",
        "partial_update": "workout.update",
        "destroy": "workout.delete",
        "complete": "workout.update",
        "cancel": "workout.update",
    }

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        member_plan = AssignmentService.assign_template(
            member=serializer.validated_data["member"],
            workout_template=serializer.validated_data[
                "workout_template"
            ],
            trainer=serializer.validated_data.get(
                "trainer"
            ),
            assigned_by=request.user,
            assignment_type=serializer.validated_data.get(
                "assignment_type",
                "GENERAL",
            ),
            source=serializer.validated_data.get(
                "source",
                "TEMPLATE",
            ),
            start_date=serializer.validated_data.get(
                "start_date"
            ),
            notes=serializer.validated_data.get(
                "notes",
                "",
            ),
        )

        output_serializer = self.get_serializer(
            member_plan
        )

        return Response(
            output_serializer.data,
            status=status.HTTP_201_CREATED,
        )

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):

        plan = self.get_object()

        AssignmentService.complete_plan(
            member_plan=plan,
        )

        return Response(
            MemberWorkoutPlanSerializer(plan).data
        )

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):

        plan = self.get_object()

        AssignmentService.cancel_plan(
            member_plan=plan,
        )

        return Response(
            MemberWorkoutPlanSerializer(plan).data
        )