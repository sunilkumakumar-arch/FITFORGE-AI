from django.contrib import admin

from workouts.models import (
    WorkoutLog,
    ExerciseLog,
)


class ExerciseLogInline(admin.TabularInline):
    model = ExerciseLog
    extra = 0
    readonly_fields = (
        "workout_exercise",
        "sets_completed",
        "reps_completed",
        "weight_used",
        "rpe",
    )


@admin.register(WorkoutLog)
class WorkoutLogAdmin(admin.ModelAdmin):

    list_display = (
        "member_workout",
        "workout_date",
        "status",
        "duration_minutes",
        "calories_burned",
    )

    list_filter = (
        "status",
        "workout_date",
    )

    search_fields = (
        "member_workout__member__first_name",
        "member_workout__member__last_name",
    )

    inlines = [
        ExerciseLogInline,
    ]


@admin.register(ExerciseLog)
class ExerciseLogAdmin(admin.ModelAdmin):

    list_display = (
        "workout_log",
        "workout_exercise",
        "sets_completed",
        "reps_completed",
        "weight_used",
    )

    search_fields = (
        "workout_exercise__exercise__name",
    )

    list_filter = (
        "completed",
    )