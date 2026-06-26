from django.contrib import admin
from .models import MembershipPlan, MemberMembership


@admin.register(MembershipPlan)
class MembershipPlanAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "duration_days",
        "price",
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
    )


@admin.register(MemberMembership)
class MemberMembershipAdmin(admin.ModelAdmin):
    list_display = (
        "member",
        "plan",
        "status",
        "start_date",
        "end_date",
        "amount_paid",
    )

    list_filter = (
        "status",
        "plan",
    )

    search_fields = (
        "member__first_name",
        "member__last_name",
        "member__phone",
    )
