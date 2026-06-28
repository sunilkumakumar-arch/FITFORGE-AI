from rest_framework import serializers

from .models import (
    NutritionPlan,
    Meal,
    MemberNutritionAssignment,
)


class NutritionPlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = NutritionPlan
        fields = "__all__"


class MealSerializer(serializers.ModelSerializer):

    class Meta:
        model = Meal
        fields = "__all__"


class MemberNutritionAssignmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = MemberNutritionAssignment
        fields = "__all__"