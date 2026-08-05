from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
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
    permission_classes = [IsAuthenticated]

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