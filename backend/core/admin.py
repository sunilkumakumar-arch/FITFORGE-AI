from django.contrib import admin

from .models import (
    Organization,
    Branch,
    Department,
    Designation,
    Role,
    Shift,
)


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "owner_name",
        "email",
        "phone",
    )

    search_fields = (
        "name",
        "owner_name",
        "email",
    )

    ordering = ("name",)


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "organization",
        "city",
    )

    list_filter = (
        "organization",
    )

    search_fields = (
        "name",
        "city",
    )

    ordering = (
        "organization",
        "name",
    )


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "name",
    )


@admin.register(Designation)
class DesignationAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "department",
        "hierarchy_level",
        "is_active",
    )

    list_filter = (
        "department",
        "is_active",
    )

    search_fields = (
        "name",
        "department__name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "department",
        "hierarchy_level",
        "name",
    )


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
    )

    ordering = (
        "name",
    )


@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "shift_type",
        "start_time",
        "end_time",
        "weekly_working_days",
        "is_active",
    )

    list_filter = (
        "shift_type",
        "is_active",
    )

    search_fields = (
        "name",
        "code",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "name",
    )