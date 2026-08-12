from rest_framework import serializers

from .models import (
    GymFacility,
    GymZone,
    Equipment,
    EquipmentMaintenance,
)


class GymFacilitySerializer(serializers.ModelSerializer):

    branch_name = serializers.CharField(
        source="branch.name",
        read_only=True,
    )

    organization_id = serializers.IntegerField(
        source="branch.organization_id",
        read_only=True,
    )

    class Meta:
        model = GymFacility

        fields = [
            "id",
            "name",
            "code",
            "branch",
            "branch_name",
            "organization_id",
            "description",
            "capacity",
            "area_sqft",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "branch_name",
            "organization_id",
            "created_at",
            "updated_at",
        ]

    def validate_capacity(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Facility capacity cannot be negative."
            )

        return value

    def validate_area_sqft(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Facility area cannot be negative."
            )

        return value


class GymZoneSerializer(serializers.ModelSerializer):

    facility_name = serializers.CharField(
        source="facility.name",
        read_only=True,
    )

    branch_id = serializers.IntegerField(
        source="facility.branch_id",
        read_only=True,
    )

    organization_id = serializers.IntegerField(
        source="facility.branch.organization_id",
        read_only=True,
    )

    class Meta:
        model = GymZone

        fields = [
            "id",
            "facility",
            "facility_name",
            "branch_id",
            "organization_id",
            "name",
            "code",
            "zone_type",
            "capacity",
            "description",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "facility_name",
            "branch_id",
            "organization_id",
            "created_at",
            "updated_at",
        ]

    def validate_capacity(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Zone capacity cannot be negative."
            )

        return value


class EquipmentSerializer(serializers.ModelSerializer):

    branch_name = serializers.CharField(
        source="branch.name",
        read_only=True,
    )

    organization_id = serializers.IntegerField(
        source="branch.organization_id",
        read_only=True,
    )

    zone_name = serializers.CharField(
        source="zone.name",
        read_only=True,
        allow_null=True,
    )

    class Meta:
        model = Equipment

        fields = [
            "id",
            "branch",
            "branch_name",
            "organization_id",
            "zone",
            "zone_name",
            "name",
            "code",
            "category",
            "manufacturer",
            "model_number",
            "serial_number",
            "purchase_date",
            "warranty_expiry",
            "status",
            "purchase_cost",
            "notes",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "branch_name",
            "organization_id",
            "zone_name",
            "created_at",
            "updated_at",
        ]

    def validate_purchase_cost(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Equipment purchase cost cannot be negative."
            )

        return value

    def validate(self, attrs):

        purchase_date = attrs.get(
            "purchase_date"
        )

        warranty_expiry = attrs.get(
            "warranty_expiry"
        )

        if (
            purchase_date
            and warranty_expiry
            and warranty_expiry < purchase_date
        ):
            raise serializers.ValidationError(
                {
                    "warranty_expiry": (
                        "Warranty expiry cannot be before "
                        "the purchase date."
                    )
                }
            )

        zone = attrs.get("zone")

        branch = attrs.get("branch")

        if zone and branch:
            if zone.facility.branch_id != branch.id:
                raise serializers.ValidationError(
                    {
                        "zone": (
                            "Selected zone must belong to "
                            "the selected branch."
                        )
                    }
                )

        return attrs


class EquipmentMaintenanceSerializer(
    serializers.ModelSerializer
):

    equipment_name = serializers.CharField(
        source="equipment.name",
        read_only=True,
    )

    branch_id = serializers.IntegerField(
        source="equipment.branch_id",
        read_only=True,
    )

    organization_id = serializers.IntegerField(
        source="equipment.branch.organization_id",
        read_only=True,
    )

    class Meta:
        model = EquipmentMaintenance

        fields = [
            "id",
            "equipment",
            "equipment_name",
            "branch_id",
            "organization_id",
            "maintenance_type",
            "scheduled_date",
            "completed_date",
            "vendor",
            "cost",
            "status",
            "notes",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "equipment_name",
            "branch_id",
            "organization_id",
            "created_at",
            "updated_at",
        ]

    def validate_cost(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Maintenance cost cannot be negative."
            )

        return value

    def validate(self, attrs):

        scheduled_date = attrs.get(
            "scheduled_date"
        )

        completed_date = attrs.get(
            "completed_date"
        )

        if (
            scheduled_date
            and completed_date
            and completed_date < scheduled_date
        ):
            raise serializers.ValidationError(
                {
                    "completed_date": (
                        "Completed date cannot be before "
                        "the scheduled date."
                    )
                }
            )

        return attrs