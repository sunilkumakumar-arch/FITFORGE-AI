from django.contrib import admin

from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):

    list_display = (
        "employee_code",
        "first_name",
        "last_name",
        "employee_classification",
        "designation",
        "branch",
        "employment_type",
        "employment_status",
        "joining_date",
    )

    list_filter = (
        "organization",
        "branch",
        "department",
        "designation",
        "employee_classification",
        "employment_type",
        "employment_status",
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
                    "employee_code",
                    "first_name",
                    "last_name",
                    "date_of_birth",
                    "gender",
                    "email",
                    "phone",
                    "alternate_phone",
                    "profile_photo",
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
                    "designation",
                    "role",
                )
            },
        ),
        (
            "Employment",
            {
                "fields": (
                    "employment_type",
                    "employee_classification",
                    "joining_date",
                    "confirmation_date",
                    "relieving_date",
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
            "Government & Documents",
            {
                "fields": (
                    "aadhaar_number",
                    "aadhaar_document",
                    "pan_number",
                    "pan_document",
                    "resume",
                    "appointment_letter",
                )
            },
        ),
        (
            "Address",
            {
                "fields": (
                    "address",
                    "city",
                    "state",
                    "pincode",
                    "blood_group",
                )
            },
        ),
        (
            "Payroll",
            {
                "fields": (
                    "salary",
                )
            },
        ),
        (
            "Additional Information",
            {
                "fields": (
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