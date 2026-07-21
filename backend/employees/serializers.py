from rest_framework import serializers

from .models import Employee

from datetime import date
import re


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            "id",
            "employee_code",

            # Personal Information
            "first_name",
            "last_name",
            "email",
            "phone",

            # Organization Information
            "organization",
            "branch",
            "department",
            "designation",
            "role",

            # Employment Information
            "joining_date",
            "confirmation_date",
            "relieving_date",
            "employment_status",
            "employment_type",
            "employee_classification",

            # Additional Information
            "profile_photo",
            "emergency_contact_name",
            "emergency_contact_phone",
            "notes",

            # System Fields
            "created_at",
            "updated_at",
        ]

        read_only_fields = (
            "employee_code",
            "created_at",
            "updated_at",
        )

    def validate_first_name(self, value):
        value = value.strip()

        if len(value) < 2:
            raise serializers.ValidationError(
                "First name must contain at least 2 characters."
            )

        if not re.match(r"^[A-Za-z ]+$", value):
            raise serializers.ValidationError(
                "First name can contain only letters."
            )

        return value.title() 
    
    def validate_last_name(self, value):
        value = value.strip()

        if len(value) < 2:
            raise serializers.ValidationError(
                "Last name must contain at least 2 characters."
            )

        if not re.match(r"^[A-Za-z ]+$", value):
            raise serializers.ValidationError(
                "Last name can contain only letters."
            )

        return value.title()
    

    def validate_phone(self, value):
        if not re.fullmatch(r"[6-9]\d{9}", value):
            raise serializers.ValidationError(
                "Enter a valid 10-digit mobile number."
            )

        return value
    
    def validate_joining_date(self, value):
        if value > date.today():
            raise serializers.ValidationError(
                "Joining date cannot be in the future."
            )

        return value