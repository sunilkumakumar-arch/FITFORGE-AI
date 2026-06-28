from django.contrib import admin
from .models import (
    NutritionPlan,
    Meal,
    MemberNutritionAssignment,
)


@admin.register(NutritionPlan)
class NutritionPlanAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "goal",
        "calories",
        "protein",
        "carbs",
        "fats",
        "created_by",
    )

    list_filter = (
        "goal",
    )

    search_fields = (
        "name",
    )


@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):

    list_display = (
        "meal_name",
        "nutrition_plan",
        "meal_time",
        "calories",
    )

    search_fields = (
        "meal_name",
    )


@admin.register(MemberNutritionAssignment)
class MemberNutritionAssignmentAdmin(admin.ModelAdmin):

    list_display = (
        "member",
        "nutrition_plan",
        "assigned_by",
        "assigned_date",
        "active",
    )

    list_filter = (
        "active",
    )

    search_fields = (
        "member__first_name",
        "member__last_name",
    )