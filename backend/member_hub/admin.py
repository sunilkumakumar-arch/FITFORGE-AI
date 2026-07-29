from django.contrib import admin

from .models import MemberHub


@admin.register(MemberHub)
class MemberHubAdmin(admin.ModelAdmin):

    list_display = (
        "public_member_id",
        "member",
        "card_level",
        "card_version",
        "created_at",
    )

    search_fields = (
        "public_member_id",
        "member__member_code",
        "member__first_name",
        "member__last_name",
        "member__phone",
        "member__email",
    )

    readonly_fields = (
        "public_member_id",
        "qr_token",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "card_level",
        "card_version",
    )

    autocomplete_fields = (
        "member",
    )

    ordering = (
        "member__member_code",
    )