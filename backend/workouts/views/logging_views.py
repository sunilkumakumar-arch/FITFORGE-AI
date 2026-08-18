from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets

from rest_framework.decorators import action
from roles.permissions import RolePermission
from rest_framework.response import Response

from workouts.models import (
    WorkoutLog,
    WorkoutExercise,
)
from workouts.serializers import (
    WorkoutLogSerializer,
    StartWorkoutSerializer,
    ExerciseLogCreateSerializer,
    ExerciseLogSerializer,
)
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
    permission_classes = [RolePermission]

    permission_map = {
        "list": "workout.view",
        "retrieve": "workout.view",
        "create": "workout.create",
        "update": "workout.update",
        "partial_update": "workout.update",
        "destroy": "workout.delete",
        "log_exercise": "workout.update",
        "finish": "workout.update",
    }

    def create(self, request, *args, **kwargs):
        """
        Start a workout session.
        """

        serializer = StartWorkoutSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        member_workout_day = (
            serializer.validated_data["workout_day"]
        )

        workout_log = (
            WorkoutLoggingService.start_workout(
                member_workout_day=member_workout_day,
            )
        )

        return Response(
            WorkoutLogSerializer(workout_log).data,
            status=status.HTTP_201_CREATED,
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="exercises",
    )
    def log_exercise(self, request, pk=None):
        """
        Log an exercise against a workout session.
        """

        workout_log = self.get_object()

        serializer = ExerciseLogCreateSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        from workouts.models import WorkoutExercise

        workout_exercise = get_object_or_404(
            WorkoutExercise,
            id=serializer.validated_data[
                "workout_exercise"
            ],

        )

        exercise_log = (
            WorkoutLoggingService.log_exercise(
                workout_log=workout_log,
                workout_exercise=workout_exercise,
                sets_completed=serializer.validated_data[
                    "sets_completed"
                ],
                reps_completed=serializer.validated_data[
                    "reps_completed"
                ],
                weight_used=serializer.validated_data[
                    "weight_used"
                ],
                rpe=serializer.validated_data.get(
                    "rpe"
                ),
                notes=serializer.validated_data.get(
                    "notes",
                    "",
                ),
            )
        )

        return Response(
            ExerciseLogSerializer(
                exercise_log
            ).data,
            status=status.HTTP_201_CREATED,
        )

    @action(
        detail=True,
        methods=["post"],
    )
    def finish(self, request, pk=None):
        """
        Complete a workout session.
        """

        workout_log = self.get_object()

        duration_minutes = request.data.get(
            "duration_minutes",
            0,
        )

        calories_burned = request.data.get(
            "calories_burned",
            0,
        )

        notes = request.data.get(
            "notes",
            "",
        )

        WorkoutLoggingService.complete_workout(
            workout_log=workout_log,
            duration_minutes=duration_minutes,
            calories_burned=calories_burned,
            notes=notes,
        )

        workout_log.refresh_from_db()

        return Response(
            WorkoutLogSerializer(
                workout_log
            ).data,
            status=status.HTTP_200_OK,
        )