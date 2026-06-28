from rest_framework import serializers

from .models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            "id",
            "employee_code",
            "first_name",
            "last_name",
            "email",
            "phone",
            "organization",
            "branch",
            "department",
            "role",
            "joining_date",
            "employment_status",
            "profile_photo",
            "emergency_contact_name",
            "emergency_contact_phone",
            "notes",
            "created_at",
            "updated_at",
   ]
        
    read_only_fields = (
        "employee_code",
        "created_at",
        "updated_at",
    )