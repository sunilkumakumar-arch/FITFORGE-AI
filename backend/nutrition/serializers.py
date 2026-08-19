from rest_framework import serializers

from .models import (
    NutritionPlan,
    Meal,
    MemberNutritionAssignment,
)


class NutritionPlanSerializer(serializers.ModelSerializer):

    created_by_name = serializers.CharField(
        source="created_by.first_name",
        read_only=True,
    )

    class Meta:
        model = NutritionPlan

        fields = [
            "id",
            "name",
            "goal",
            "calories",
            "protein",
            "carbs",
            "fats",
            "notes",
            "created_by",
            "created_by_name",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_by",
            "created_by_name",
            "created_at",
            "updated_at",
        ]


class MealSerializer(serializers.ModelSerializer):

    class Meta:
        model = Meal

        fields = [
            "id",
            "nutrition_plan",
            "meal_name",
            "meal_time",
            "foods",
            "calories",
        ]

        read_only_fields = [
            "id",
        ]


class MemberNutritionAssignmentSerializer(
    serializers.ModelSerializer
):

    member_name = serializers.CharField(
        source="member.first_name",
        read_only=True,
    )

    nutrition_plan_name = serializers.CharField(
        source="nutrition_plan.name",
        read_only=True,
    )

    assigned_by_name = serializers.CharField(
        source="assigned_by.first_name",
        read_only=True,
    )

    class Meta:
        model = MemberNutritionAssignment

        fields = [
            "id",
            "member",
            "member_name",
            "nutrition_plan",
            "nutrition_plan_name",
            "assigned_by",
            "assigned_by_name",
            "assigned_date",
            "active",
        ]

        read_only_fields = [
            "id",
            "assigned_by",
            "assigned_by_name",
            "assigned_date",
        ]