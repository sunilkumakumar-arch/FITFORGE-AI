from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from workouts.models import Exercise
from workouts.serializers.exercise_serializer import ExerciseSerializer


class ExerciseViewSet(viewsets.ModelViewSet):
    """
    CRUD API for Exercise Library.
    """

    queryset = (
        Exercise.objects
        .select_related(
            "muscle_group",
            "category",
        )
        .all()
        .order_by("name")
    )

    serializer_class = ExerciseSerializer

    permission_classes = [
        IsAuthenticated,
    ]

    filterset_fields = [
        "muscle_group",
        "category",
        "difficulty",
        "is_active",
    ]

    search_fields = [
        "name",
        "description",
    ]

    ordering_fields = [
        "name",
        "difficulty",
    ]