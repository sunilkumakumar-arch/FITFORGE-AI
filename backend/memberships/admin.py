from django.contrib import admin

from .models import (
    MembershipPlan,
    MemberMembership,
)


@admin.register(MembershipPlan)
class MembershipPlanAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "code",
        "organization",
        "branch",
        "duration_days",
        "price",
        "joining_fee",
        "freeze_days_allowed",
        "pt_sessions_included",
        "is_active",
        "created_at",
    )

    list_filter = (
        "organization",
        "branch",
        "is_active",
    )

    search_fields = (
        "name",
        "code",
        "organization__name",
        "branch__name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    autocomplete_fields = (
        "organization",
        "branch",
    )

    ordering = (
        "organization",
        "branch",
        "name",
    )

    list_per_page = 25

    fieldsets = (
        (
            "Plan Information",
            {
                "fields": (
                    "name",
                    "code",
                    "organization",
                    "branch",
                )
            },
        ),
        (
            "Pricing & Duration",
            {
                "fields": (
                    "duration_days",
                    "price",
                    "joining_fee",
                )
            },
        ),
        (
            "Benefits & Restrictions",
            {
                "fields": (
                    "freeze_days_allowed",
                    "pt_sessions_included",
                    "description",
                )
            },
        ),
        (
            "Status",
            {
                "fields": (
                    "is_active",
                )
            },
        ),
        (
            "System Information",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )


@admin.register(MemberMembership)
class MemberMembershipAdmin(admin.ModelAdmin):

    list_display = (
        "member",
        "plan",
        "status",
        "start_date",
        "end_date",
        "remaining_days_display",
        "amount_paid",
        "payment_reference",
        "created_at",
    )

    list_filter = (
        "status",
        "plan",
        "start_date",
        "end_date",
    )

    search_fields = (
        "member__first_name",
        "member__last_name",
        "member__phone",
        "plan__name",
        "plan__code",
        "payment_reference",
    )

    readonly_fields = (
        "remaining_days_display",
        "created_at",
        "updated_at",
    )

    autocomplete_fields = (
        "member",
        "plan",
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 25

    fieldsets = (
        (
            "Member & Plan",
            {
                "fields": (
                    "member",
                    "plan",
                )
            },
        ),
        (
            "Membership Period",
            {
                "fields": (
                    "start_date",
                    "end_date",
                    "status",
                    "remaining_days_display",
                )
            },
        ),
        (
            "Payment",
            {
                "fields": (
                    "amount_paid",
                    "payment_reference",
                )
            },
        ),
        (
            "System Information",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    @admin.display(
        description="Days Left",
        ordering="end_date",
    )
    def remaining_days_display(self, obj):
        return obj.remaining_days