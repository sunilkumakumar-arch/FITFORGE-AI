from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import (
    WorkoutPlan,
    WorkoutDay,
    WorkoutExercise,
    MemberWorkoutAssignment,
)

from .serializers import (
    WorkoutPlanSerializer,
    WorkoutDaySerializer,
    WorkoutExerciseSerializer,
    MemberWorkoutAssignmentSerializer,
)


class WorkoutPlanViewSet(viewsets.ModelViewSet):

    queryset = WorkoutPlan.objects.all()

    serializer_class = WorkoutPlanSerializer

    permission_classes = [IsAuthenticated]


class WorkoutDayViewSet(viewsets.ModelViewSet):

    queryset = WorkoutDay.objects.all()

    serializer_class = WorkoutDaySerializer

    permission_classes = [IsAuthenticated]


class WorkoutExerciseViewSet(viewsets.ModelViewSet):

    queryset = WorkoutExercise.objects.all()

    serializer_class = WorkoutExerciseSerializer

    permission_classes = [IsAuthenticated]


class MemberWorkoutAssignmentViewSet(viewsets.ModelViewSet):

    queryset = MemberWorkoutAssignment.objects.all()

    serializer_class = MemberWorkoutAssignmentSerializer

    permission_classes = [IsAuthenticated]