from django.contrib import admin
from .models import TrainerAssignment


@admin.register(TrainerAssignment)
class TrainerAssignmentAdmin(admin.ModelAdmin):
    list_display = (
        "trainer",
        "member",
        "start_date",
        "end_date",
        "monthly_fee",
        "is_active",
    )

    list_filter = (
        "is_active",
        "trainer",
    )

    search_fields = (
        "trainer__first_name",
        "trainer__last_name",
        "member__first_name",
        "member__last_name",
    )