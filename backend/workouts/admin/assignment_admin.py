from django.contrib import admin

from workouts.models import (
    MemberWorkoutPlan,
    MemberWorkoutDay,
)


class MemberWorkoutDayInline(admin.TabularInline):
    model = MemberWorkoutDay
    extra = 0
    readonly_fields = (
        "workout_day",
        "completed",
        "completed_at",
    )


@admin.register(MemberWorkoutPlan)
class MemberWorkoutPlanAdmin(admin.ModelAdmin):

    list_display = (
        "member",
        "workout_template",
        "trainer",
        "assignment_type",
        "status",
        "start_date",
        "end_date",
    )

    list_filter = (
        "status",
        "assignment_type",
        "source",
    )

    search_fields = (
        "member__first_name",
        "member__last_name",
        "workout_template__name",
    )

    readonly_fields = (
        "version",
        "created_at",
        "updated_at",
    )

    inlines = [
        MemberWorkoutDayInline,
    ]


@admin.register(MemberWorkoutDay)
class MemberWorkoutDayAdmin(admin.ModelAdmin):

    list_display = (
        "member_workout",
        "workout_day",
        "completed",
        "completed_at",
    )

    list_filter = (
        "completed",
    )

    search_fields = (
        "member_workout__member__first_name",
        "member_workout__member__last_name",
    )