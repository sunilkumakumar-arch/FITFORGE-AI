# leads/admin.py

from django.contrib import admin

from .models import (
    Lead,
    LeadFollowUp
)


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):

    list_display = (
        "first_name",
        "phone",
        "source",
        "status",
        "created_at",
    )

    list_filter = (
        "source",
        "status",
    )

    search_fields = (
        "first_name",
        "last_name",
        "phone",
        "email",
    )


@admin.register(LeadFollowUp)
class LeadFollowUpAdmin(
    admin.ModelAdmin
):

    list_display = (
        "lead",
        "followup_date",
        "next_followup_date",
    )