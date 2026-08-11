from datetime import date
from decimal import Decimal
import re

from rest_framework import serializers

from .models import Employee


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
            "date_of_birth",
            "gender",
            "alternate_phone",
            "aadhaar_number",
            "pan_number",

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
            "address",
            "city",
            "state",
            "pincode",
            "blood_group",
            "salary",

            # Documents
            "aadhaar_document",
            "pan_document",
            "resume",
            "appointment_letter",

            # System Fields
            "created_at",
            "updated_at",
        ]

        read_only_fields = (
            "employee_code",
            "created_at",
            "updated_at",
        )

    # ---------------------------------------------------------
    # PERSONAL VALIDATION
    # ---------------------------------------------------------

    def validate_first_name(self, value):

        value = value.strip()

        if len(value) < 2:
            raise serializers.ValidationError(
                "First name must contain at least 2 characters."
            )

        if not re.fullmatch(r"[A-Za-z ]+", value):
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

        if not re.fullmatch(r"[A-Za-z ]+", value):
            raise serializers.ValidationError(
                "Last name can contain only letters."
            )

        return value.title()

    def validate_phone(self, value):

        value = value.strip()

        if not re.fullmatch(r"[6-9]\d{9}", value):
            raise serializers.ValidationError(
                "Enter a valid 10-digit mobile number."
            )

        return value

    def validate_alternate_phone(self, value):

        value = value.strip()

        if not value:
            return value

        if not re.fullmatch(r"[6-9]\d{9}", value):
            raise serializers.ValidationError(
                "Enter a valid 10-digit alternate mobile number."
            )

        return value

    def validate_emergency_contact_phone(self, value):

        value = value.strip()

        if not value:
            return value

        if not re.fullmatch(r"[6-9]\d{9}", value):
            raise serializers.ValidationError(
                "Enter a valid 10-digit emergency contact number."
            )

        return value

    # ---------------------------------------------------------
    # IDENTITY VALIDATION
    # ---------------------------------------------------------

    def validate_aadhaar_number(self, value):

        value = value.strip()

        if not value:
            return value

        if not re.fullmatch(r"\d{12}", value):
            raise serializers.ValidationError(
                "Aadhaar number must contain exactly 12 digits."
            )

        return value

    def validate_pan_number(self, value):

        value = value.strip().upper()

        if not value:
            return value

        if not re.fullmatch(
            r"[A-Z]{5}[0-9]{4}[A-Z]",
            value,
        ):
            raise serializers.ValidationError(
                "Enter a valid PAN number."
            )

        return value

    # ---------------------------------------------------------
    # DATE VALIDATION
    # ---------------------------------------------------------

    def validate_date_of_birth(self, value):

        if value > date.today():
            raise serializers.ValidationError(
                "Date of birth cannot be in the future."
            )

        return value

    def validate_joining_date(self, value):

        if value > date.today():
            raise serializers.ValidationError(
                "Joining date cannot be in the future."
            )

        return value

    # ---------------------------------------------------------
    # FINANCIAL VALIDATION
    # ---------------------------------------------------------

    def validate_salary(self, value):

        if value < Decimal("0"):
            raise serializers.ValidationError(
                "Salary cannot be negative."
            )

        return value

    # ---------------------------------------------------------
    # LOCATION VALIDATION
    # ---------------------------------------------------------

    def validate_pincode(self, value):

        value = value.strip()

        if not value:
            return value

        if not re.fullmatch(r"\d{6}", value):
            raise serializers.ValidationError(
                "Pincode must contain exactly 6 digits."
            )

        return value

    # ---------------------------------------------------------
    # EMPLOYEE BUSINESS VALIDATION
    # ---------------------------------------------------------

    def validate(self, attrs):

        organization = attrs.get(
            "organization",
            getattr(
                self.instance,
                "organization",
                None,
            )
            if self.instance
            else None,
        )

        branch = attrs.get(
            "branch",
            getattr(
                self.instance,
                "branch",
                None,
            )
            if self.instance
            else None,
        )

        joining_date = attrs.get(
            "joining_date",
            getattr(
                self.instance,
                "joining_date",
                None,
            )
            if self.instance
            else None,
        )

        confirmation_date = attrs.get(
            "confirmation_date",
            getattr(
                self.instance,
                "confirmation_date",
                None,
            )
            if self.instance
            else None,
        )

        relieving_date = attrs.get(
            "relieving_date",
            getattr(
                self.instance,
                "relieving_date",
                None,
            )
            if self.instance
            else None,
        )

        employment_status = attrs.get(
            "employment_status",
            getattr(
                self.instance,
                "employment_status",
                None,
            )
            if self.instance
            else None,
        )

        # -----------------------------------------------------
        # ORGANIZATION → BRANCH INTEGRITY
        # -----------------------------------------------------

        if organization and branch:

            if branch.organization_id != organization.id:

                raise serializers.ValidationError(
                    {
                        "branch": (
                            "Selected branch does not belong "
                            "to the selected organization."
                        )
                    }
                )

        # -----------------------------------------------------
        # EMPLOYMENT DATE INTEGRITY
        # -----------------------------------------------------

        if joining_date and confirmation_date:

            if confirmation_date < joining_date:

                raise serializers.ValidationError(
                    {
                        "confirmation_date": (
                            "Confirmation date cannot be "
                            "before the joining date."
                        )
                    }
                )

        if joining_date and relieving_date:

            if relieving_date < joining_date:

                raise serializers.ValidationError(
                    {
                        "relieving_date": (
                            "Relieving date cannot be "
                            "before the joining date."
                        )
                    }
                )

        if confirmation_date and relieving_date:

            if relieving_date < confirmation_date:

                raise serializers.ValidationError(
                    {
                        "relieving_date": (
                            "Relieving date cannot be "
                            "before the confirmation date."
                        )
                    }
                )

        # -----------------------------------------------------
        # ACTIVE EMPLOYEE INTEGRITY
        # -----------------------------------------------------

        if (
            employment_status == "ACTIVE"
            and relieving_date
        ):

            raise serializers.ValidationError(
                {
                    "relieving_date": (
                        "An active employee cannot have "
                        "a relieving date."
                    )
                }
            )

        return attrs