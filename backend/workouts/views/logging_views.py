from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from roles.permissions import RolePermission

from accounts.models import Member

from workouts.models import (
    WorkoutLog,
    WorkoutExercise,
    Exercise,
)

from workouts.serializers import (
    WorkoutLogSerializer,
    StartWorkoutSerializer,
    ExerciseLogCreateSerializer,
    ExerciseLogSerializer,
    ExerciseHistorySerializer,
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
        "exercise_history": "workout.view",
        "finish": "workout.update",
    }

    # =====================================================
    # Start Workout
    # =====================================================

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

    # =====================================================
    # Log Exercise
    # =====================================================

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

    # =====================================================
    # Exercise Performance History
    # =====================================================

    @action(
        detail=False,
        methods=["get"],
        url_path="exercise-history",
    )
    def exercise_history(self, request):
        """
        Return exercise performance history for a member.
        """

        member_id = request.query_params.get(
            "member"
        )

        exercise_id = request.query_params.get(
            "exercise"
        )

        if not member_id:
            return Response(
                {
                    "member": (
                        "This query parameter is required."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not exercise_id:
            return Response(
                {
                    "exercise": (
                        "This query parameter is required."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        member = Member.objects.filter(
            id=member_id
        ).first()

        if not member:
            return Response(
                {
                    "member": "Member not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        exercise = Exercise.objects.filter(
            id=exercise_id
        ).first()

        if not exercise:
            return Response(
                {
                    "exercise": "Exercise not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        history = (
            WorkoutLoggingService.get_exercise_history(
                member=member,
                exercise=exercise,
            )
        )

        return Response(
            ExerciseHistorySerializer(
                history,
                many=True,
            ).data,
            status=status.HTTP_200_OK,
        )

    # =====================================================
    # Finish Workout
    # =====================================================

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