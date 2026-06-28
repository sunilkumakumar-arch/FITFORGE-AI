from django.contrib import admin

from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):

    list_display = (
        "employee_code",
        "first_name",
        "last_name",
        "email",
        "phone",
        "branch",
        "role",
        "employment_status",
        "joining_date",
    )

    list_filter = (
        "employment_status",
        "organization",
        "branch",
        "department",
        "role",
    )

    search_fields = (
        "employee_code",
        "first_name",
        "last_name",
        "email",
        "phone",
    )

    readonly_fields = (
        "employee_code",
        "created_at",
        "updated_at",
    )

    list_per_page = 25

    ordering = ("employee_code",)

    fieldsets = (
        (
            "Employee Information",
            {
                "fields": (
                    
                    "first_name",
                    "last_name",
                    "email",
                    "phone",
                )
            },
        ),
        (
            "Organization",
            {
                "fields": (
                    "organization",
                    "branch",
                    "department",
                    "role",
                )
            },
        ),
        (
            "Employment",
            {
                "fields": (
                    "joining_date",
                    "employment_status",
                )
            },
        ),
        (
            "Emergency Contact",
            {
                "fields": (
                    "emergency_contact_name",
                    "emergency_contact_phone",
                )
            },
        ),
        (
            "Additional Information",
            {
                "fields": (
                    "profile_photo",
                    "notes",
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