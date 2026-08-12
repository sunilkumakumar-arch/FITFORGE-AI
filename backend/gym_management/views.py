from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from roles.permissions import RolePermission

from .models import (
    GymFacility,
    GymZone,
    Equipment,
    EquipmentMaintenance,
)
from .serializers import (
    GymFacilitySerializer,
    GymZoneSerializer,
    EquipmentSerializer,
    EquipmentMaintenanceSerializer,
)


class GymFacilityViewSet(viewsets.ModelViewSet):
    """
    Enterprise Gym Facility Management API.
    """

    queryset = (
        GymFacility.objects
        .select_related(
            "branch",
            "branch__organization",
        )
        .all()
        .order_by("name")
    )

    serializer_class = GymFacilitySerializer

    permission_classes = [
        RolePermission,
    ]

    permission_map = {
        "list": "gym_management.view",
        "retrieve": "gym_management.view",
        "create": "gym_management.create",
        "update": "gym_management.update",
        "partial_update": "gym_management.update",
        "destroy": "gym_management.delete",
    }

    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )

    filterset_fields = (
        "branch",
        "branch__organization",
        "is_active",
    )

    search_fields = (
        "name",
        "code",
        "description",
        "branch__name",
        "branch__organization__name",
    )

    ordering_fields = (
        "name",
        "code",
        "capacity",
        "area_sqft",
        "created_at",
        "updated_at",
    )

    ordering = (
        "name",
    )

    def get_queryset(self):
        queryset = super().get_queryset()

        user = self.request.user

        if not user.is_authenticated:
            return queryset.none()

        if user.is_superuser:
            return queryset

        try:
            employee = (
                user.employee_profile
            )
        except Exception:
            return queryset.none()

        if not employee.role:
            return queryset.none()

        role_code = employee.role.code

        if role_code == "SUPER_ADMIN":
            return queryset

        if role_code == "ORG_OWNER":
            if not employee.organization_id:
                return queryset.none()

            return queryset.filter(
                branch__organization_id=employee.organization_id
            )

        if role_code == "BRANCH_MANAGER":
            if not employee.branch_id:
                return queryset.none()

            return queryset.filter(
                branch_id=employee.branch_id
            )

        return queryset.none()


class GymZoneViewSet(viewsets.ModelViewSet):
    """
    Enterprise Gym Zone Management API.
    """

    queryset = (
        GymZone.objects
        .select_related(
            "facility",
            "facility__branch",
            "facility__branch__organization",
        )
        .all()
        .order_by("name")
    )

    serializer_class = GymZoneSerializer

    permission_classes = [
        RolePermission,
    ]

    permission_map = {
        "list": "gym_management.view",
        "retrieve": "gym_management.view",
        "create": "gym_management.create",
        "update": "gym_management.update",
        "partial_update": "gym_management.update",
        "destroy": "gym_management.delete",
    }

    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )

    filterset_fields = (
        "facility",
        "facility__branch",
        "facility__branch__organization",
        "zone_type",
        "is_active",
    )

    search_fields = (
        "name",
        "code",
        "description",
        "facility__name",
        "facility__branch__name",
        "facility__branch__organization__name",
    )

    ordering_fields = (
        "name",
        "code",
        "zone_type",
        "capacity",
        "created_at",
        "updated_at",
    )

    ordering = (
        "name",
    )

    def get_queryset(self):
        queryset = super().get_queryset()

        user = self.request.user

        if not user.is_authenticated:
            return queryset.none()

        if user.is_superuser:
            return queryset

        try:
            employee = user.employee_profile
        except Exception:
            return queryset.none()

        if not employee.role:
            return queryset.none()

        role_code = employee.role.code

        if role_code == "SUPER_ADMIN":
            return queryset

        if role_code == "ORG_OWNER":
            if not employee.organization_id:
                return queryset.none()

            return queryset.filter(
                facility__branch__organization_id=(
                    employee.organization_id
                )
            )

        if role_code == "BRANCH_MANAGER":
            if not employee.branch_id:
                return queryset.none()

            return queryset.filter(
                facility__branch_id=employee.branch_id
            )

        return queryset.none()


class EquipmentViewSet(viewsets.ModelViewSet):
    """
    Enterprise Equipment Management API.
    """

    queryset = (
        Equipment.objects
        .select_related(
            "branch",
            "branch__organization",
            "zone",
            "zone__facility",
        )
        .all()
        .order_by("name")
    )

    serializer_class = EquipmentSerializer

    permission_classes = [
        RolePermission,
    ]

    permission_map = {
        "list": "gym_management.view",
        "retrieve": "gym_management.view",
        "create": "gym_management.create",
        "update": "gym_management.update",
        "partial_update": "gym_management.update",
        "destroy": "gym_management.delete",
    }

    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )

    filterset_fields = (
        "branch",
        "branch__organization",
        "zone",
        "status",
        "category",
        "is_active",
    )

    search_fields = (
        "name",
        "code",
        "manufacturer",
        "model_number",
        "serial_number",
        "notes",
        "branch__name",
        "branch__organization__name",
        "zone__name",
    )

    ordering_fields = (
        "name",
        "code",
        "category",
        "status",
        "purchase_date",
        "warranty_expiry",
        "purchase_cost",
        "created_at",
        "updated_at",
    )

    ordering = (
        "name",
    )

    def get_queryset(self):
        queryset = super().get_queryset()

        user = self.request.user

        if not user.is_authenticated:
            return queryset.none()

        if user.is_superuser:
            return queryset

        try:
            employee = user.employee_profile
        except Exception:
            return queryset.none()

        if not employee.role:
            return queryset.none()

        role_code = employee.role.code

        if role_code == "SUPER_ADMIN":
            return queryset

        if role_code == "ORG_OWNER":
            if not employee.organization_id:
                return queryset.none()

            return queryset.filter(
                branch__organization_id=employee.organization_id
            )

        if role_code == "BRANCH_MANAGER":
            if not employee.branch_id:
                return queryset.none()

            return queryset.filter(
                branch_id=employee.branch_id
            )

        return queryset.none()


class EquipmentMaintenanceViewSet(viewsets.ModelViewSet):
    """
    Enterprise Equipment Maintenance Management API.
    """

    queryset = (
        EquipmentMaintenance.objects
        .select_related(
            "equipment",
            "equipment__branch",
            "equipment__branch__organization",
        )
        .all()
        .order_by("-scheduled_date")
    )

    serializer_class = EquipmentMaintenanceSerializer

    permission_classes = [
        RolePermission,
    ]

    permission_map = {
        "list": "gym_management.view",
        "retrieve": "gym_management.view",
        "create": "gym_management.create",
        "update": "gym_management.update",
        "partial_update": "gym_management.update",
        "destroy": "gym_management.delete",
    }

    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )

    filterset_fields = (
        "equipment",
        "equipment__branch",
        "equipment__branch__organization",
        "maintenance_type",
        "status",
    )

    search_fields = (
        "equipment__name",
        "equipment__code",
        "vendor",
        "notes",
    )

    ordering_fields = (
        "scheduled_date",
        "completed_date",
        "cost",
        "created_at",
        "updated_at",
    )

    ordering = (
        "-scheduled_date",
    )

    def get_queryset(self):
        queryset = super().get_queryset()

        user = self.request.user

        if not user.is_authenticated:
            return queryset.none()

        if user.is_superuser:
            return queryset

        try:
            employee = user.employee_profile
        except Exception:
            return queryset.none()

        if not employee.role:
            return queryset.none()

        role_code = employee.role.code

        if role_code == "SUPER_ADMIN":
            return queryset

        if role_code == "ORG_OWNER":
            if not employee.organization_id:
                return queryset.none()

            return queryset.filter(
                equipment__branch__organization_id=(
                    employee.organization_id
                )
            )

        if role_code == "BRANCH_MANAGER":
            if not employee.branch_id:
                return queryset.none()

            return queryset.filter(
                equipment__branch_id=employee.branch_id
            )

        return queryset.none()