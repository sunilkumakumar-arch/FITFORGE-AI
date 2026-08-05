from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from workouts.models import WorkoutLog
from workouts.serializers import WorkoutLogSerializer
from workouts.services.logging_service import WorkoutLoggingService


class WorkoutLogViewSet(viewsets.ModelViewSet):

    queryset = (
        WorkoutLog.objects
        .select_related(
            "member_workout",
            "workout_day",
        )
        .prefetch_related(
            "exercise_logs",
        )
        .order_by("-id")
    )

    serializer_class = WorkoutLogSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["post"])
    def finish(self, request, pk=None):

        workout_log = self.get_object()

        duration_minutes = request.data.get("duration_minutes", 0)
        calories_burned = request.data.get("calories_burned", 0)
        notes = request.data.get("notes", "")

        WorkoutLoggingService.complete_workout(
            workout_log=workout_log,
            duration_minutes=duration_minutes,
            calories_burned=calories_burned,
            notes=notes,
        )

        return Response(
            WorkoutLogSerializer(workout_log).data,
            status=status.HTTP_200_OK,
        )