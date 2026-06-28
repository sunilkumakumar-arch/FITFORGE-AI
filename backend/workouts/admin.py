from django.contrib import admin
from .models import (
    WorkoutPlan,
    WorkoutDay,
    WorkoutExercise,
    MemberWorkoutAssignment,
)


@admin.register(WorkoutPlan)
class WorkoutPlanAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "goal",
        "created_by",
        "is_active",
    )

    list_filter = (
        "goal",
        "is_active",
    )

    search_fields = (
        "name",
    )


@admin.register(WorkoutDay)
class WorkoutDayAdmin(admin.ModelAdmin):
    list_display = (
        "workout_plan",
        "day_name",
        "focus_area",
    )

    list_filter = (
        "day_name",
    )

    search_fields = (
        "workout_plan__name",
        "focus_area",
    )


@admin.register(WorkoutExercise)
class WorkoutExerciseAdmin(admin.ModelAdmin):
    list_display = (
        "exercise_name",
        "workout_day",
        "sets",
        "reps",
        "rest_seconds",
    )

    search_fields = (
        "exercise_name",
    )


@admin.register(MemberWorkoutAssignment)
class MemberWorkoutAssignmentAdmin(admin.ModelAdmin):
    list_display = (
        "member",
        "workout_plan",
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