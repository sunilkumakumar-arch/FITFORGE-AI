from rest_framework import serializers

from .models import (
    Organization,
    Branch,
    Department,
    Designation,
    Shift,

)



class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = [
            "id",
            "name",
            "owner_name",
            "email",
            "phone",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )

    def validate_name(self, value):
        value = value.strip()

        if len(value) < 3:
            raise serializers.ValidationError(
                "Organization name must contain at least 3 characters."
            )

        return value

    def validate_owner_name(self, value):
        value = value.strip()

        if len(value) < 2:
            raise serializers.ValidationError(
                "Owner name must contain at least 2 characters."
            )

        return value

    def validate_phone(self, value):
        if not value.isdigit():
            raise serializers.ValidationError(
                "Phone number must contain only digits."
            )

        if len(value) != 10:
            raise serializers.ValidationError(
                "Phone number must be exactly 10 digits."
            )

        return value


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = [
            "id",
            "organization",
            "name",
            "city",
            "address",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )

    def validate_name(self, value):
        value = value.strip()

        if len(value) < 3:
            raise serializers.ValidationError(
                "Branch name must contain at least 3 characters."
            )

        return value

    def validate_city(self, value):
        value = value.strip()

        if len(value) < 2:
            raise serializers.ValidationError(
                "City must contain at least 2 characters."
            )

        return value.title()

    def validate_address(self, value):
        value = value.strip()

        if len(value) < 5:
            raise serializers.ValidationError(
                "Address must contain at least 5 characters."
            )

        return value    

class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department

        fields = [
            "id",
            "name",
            "description",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )

    def validate_name(self, value):
        value = value.strip()

        if len(value) < 2:
            raise serializers.ValidationError(
                "Department name must contain at least 2 characters."
            )

        return value.title()

    def validate_description(self, value):
        return value.strip()

class DesignationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Designation

        fields = [
            "id",
            "department",
            "name",
            "description",
            "hierarchy_level",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )

    def validate_name(self, value):
        value = value.strip()

        if len(value) < 2:
            raise serializers.ValidationError(
                "Designation name must contain at least 2 characters."
            )

        return value.title()

    def validate_description(self, value):
        return value.strip()    


class ShiftSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shift

        fields = [
            "id",
            "name",
            "code",
            "shift_type",
            "start_time",
            "end_time",
            "grace_period_minutes",
            "break_duration_minutes",
            "minimum_working_hours",
            "weekly_working_days",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )

    def validate_name(self, value):
        value = value.strip()

        if len(value) < 2:
            raise serializers.ValidationError(
                "Shift name must contain at least 2 characters."
            )

        return value.title()

    def validate_code(self, value):
        return value.strip().upper()

    def validate(self, attrs):

        if attrs["start_time"] >= attrs["end_time"]:
            raise serializers.ValidationError(
                "Shift end time must be after start time."
            )

        return attrs
