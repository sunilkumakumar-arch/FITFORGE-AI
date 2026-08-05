from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from workouts.models import (
    WorkoutTemplate,
    WorkoutDay,
    WorkoutExercise,
)

from workouts.serializers import (
    WorkoutTemplateSerializer,
    WorkoutDaySerializer,
    WorkoutExerciseSerializer,
)


class WorkoutTemplateViewSet(viewsets.ModelViewSet):
    queryset = (
        WorkoutTemplate.objects
        .prefetch_related(
            "days",
            "days__exercises",
        )
        .all()
    )

    serializer_class = WorkoutTemplateSerializer
    permission_classes = [IsAuthenticated]


class WorkoutDayViewSet(viewsets.ModelViewSet):
    queryset = (
        WorkoutDay.objects
        .select_related("workout_template")
        .prefetch_related("exercises")
        .all()
    )

    serializer_class = WorkoutDaySerializer
    permission_classes = [IsAuthenticated]


class WorkoutExerciseViewSet(viewsets.ModelViewSet):
    queryset = (
        WorkoutExercise.objects
        .select_related(
            "workout_day",
            "exercise",
        )
        .all()
    )

    serializer_class = WorkoutExerciseSerializer
    permission_classes = [IsAuthenticated]