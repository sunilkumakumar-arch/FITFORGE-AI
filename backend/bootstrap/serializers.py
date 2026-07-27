from datetime import date

from rest_framework import serializers


class OrganizationInstallSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    owner_name = serializers.CharField(max_length=200)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=15)

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


class BranchInstallSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    city = serializers.CharField(max_length=100)
    address = serializers.CharField()

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


class AdminInstallSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=15)
    joining_date = serializers.DateField()

    def validate_joining_date(self, value):
        if value > date.today():
            raise serializers.ValidationError(
                "Joining date cannot be in the future."
            )

        return value


class BootstrapSerializer(serializers.Serializer):
    organization = OrganizationInstallSerializer()
    branch = BranchInstallSerializer()
    admin = AdminInstallSerializer()