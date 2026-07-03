# pt_packages/admin.py

from django.contrib import admin

from .models import (
    PTPackage,
    MemberPTPackage,
    PTSession,
)


@admin.register(PTPackage)
class PTPackageAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "total_sessions",
        "validity_days",
        "price",
        "is_active",
    )


@admin.register(MemberPTPackage)
class MemberPTPackageAdmin(admin.ModelAdmin):

    list_display = (
        "member",
        "package",
        "sessions_used",
        "is_active",
    )


@admin.register(PTSession)
class PTSessionAdmin(admin.ModelAdmin):

    list_display = (
        "member_package",
        "trainer",
        "session_date",
        "status",
    )