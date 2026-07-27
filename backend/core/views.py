from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import Organization
from .serializers import OrganizationSerializer
from .services import OrganizationService
from roles.permissions import RolePermission
from common.responses import (
    created_response,
    success_response,
)

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

class OrganizationViewSet(viewsets.ModelViewSet):
    """
    API endpoints for Organization Management.
    """
    permission_classes = [RolePermission]
    permission_map = {
        "list": "organization.view",
        "retrieve": "organization.view",
        "create": "organization.create",
        "update": "organization.update",
        "partial_update": "organization.update",
        "destroy": "organization.delete",
    }

    queryset = Organization.objects.filter(
        is_active=True
    ).order_by("name")
    serializer_class = OrganizationSerializer

    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )

    filterset_fields = (
        "is_active",
    )

    search_fields = (
        "name",
        "owner_name",
        "email",
        "phone",
    )

    ordering_fields = (
        "name",
        "created_at",
    )

    ordering = (
        "name",
    )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        organization = OrganizationService.create_organization(
            serializer.validated_data
        )

        response_serializer = self.get_serializer(organization)

        
        return created_response(
            data=response_serializer.data,
            message="Organization created successfully.",
        )

    def destroy(self, request, *args, **kwargs):
        """
        Soft delete an organization.
        """
        organization = self.get_object()

        OrganizationService.deactivate_organization(
            organization=organization,
            user=request.user if request.user.is_authenticated else None,
        )

        return success_response(
            message="Organization deactivated successfully.",
        )