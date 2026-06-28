from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

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


class NutritionPlanViewSet(viewsets.ModelViewSet):

    queryset = NutritionPlan.objects.all()

    serializer_class = NutritionPlanSerializer

    permission_classes = [IsAuthenticated]


class MealViewSet(viewsets.ModelViewSet):

    queryset = Meal.objects.all()

    serializer_class = MealSerializer

    permission_classes = [IsAuthenticated]


class MemberNutritionAssignmentViewSet(viewsets.ModelViewSet):

    queryset = MemberNutritionAssignment.objects.all()

    serializer_class = MemberNutritionAssignmentSerializer

    permission_classes = [IsAuthenticated]