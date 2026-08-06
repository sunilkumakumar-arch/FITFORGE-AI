from rest_framework import viewsets
from roles.permissions import RolePermission

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
        .order_by("-id")
    )

    serializer_class = WorkoutTemplateSerializer
    permission_classes = [RolePermission]

    permission_map = {
        "list": "workout.view",
        "retrieve": "workout.view",
        "create": "workout.create",
        "update": "workout.update",
        "partial_update": "workout.update",
        "destroy": "workout.delete",
    }


class WorkoutDayViewSet(viewsets.ModelViewSet):
    queryset = (
        WorkoutDay.objects
        .select_related("workout_template")
        .prefetch_related("exercises")
        .order_by("sort_order", "id")
    )
    

    serializer_class = WorkoutDaySerializer
    permission_classes = [RolePermission]

    permission_map = {
        "list": "workout.view",
        "retrieve": "workout.view",
        "create": "workout.create",
        "update": "workout.update",
        "partial_update": "workout.update",
        "destroy": "workout.delete",
    }


class WorkoutExerciseViewSet(viewsets.ModelViewSet):
    queryset = (
        WorkoutExercise.objects
        .select_related(
            "workout_day",
            "exercise",
        )
        .order_by("id")
    )

    serializer_class = WorkoutExerciseSerializer
    permission_classes = [RolePermission]

    permission_map = {
        "list": "workout.view",
        "retrieve": "workout.view",
        "create": "workout.create",
        "update": "workout.update",
        "partial_update": "workout.update",
        "destroy": "workout.delete",
    }