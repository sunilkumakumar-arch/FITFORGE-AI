from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import (
    Organization,
    Branch,
    Department,
    Designation,
    
)
from .serializers import (
    OrganizationSerializer,
    BranchSerializer,
    DepartmentSerializer,
    DesignationSerializer,
)
from .services import (
    OrganizationService,
    BranchService,
    DepartmentService,
    DesignationService,
)
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


class BranchViewSet(viewsets.ModelViewSet):
    """
    API endpoints for Branch Management.
    """

    permission_classes = [RolePermission]

    permission_map = {
        "list": "branch.view",
        "retrieve": "branch.view",
        "create": "branch.create",
        "update": "branch.update",
        "partial_update": "branch.update",
        "destroy": "branch.delete",
    }

    queryset = Branch.objects.all().order_by("name")
    serializer_class = BranchSerializer

    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )

    filterset_fields = (
        "organization",
        "city",
    )

    search_fields = (
        "name",
        "city",
    )

    ordering_fields = (
        "name",
        "created_at",
    )

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        branch = BranchService.create_branch(
            serializer.validated_data
        )

        return created_response(
            BranchSerializer(branch).data,
            "Branch created successfully."
        )

    def destroy(self, request, *args, **kwargs):

        branch = self.get_object()

        BranchService.deactivate_branch(
            branch,
            request.user
        )

        return success_response(
            message="Branch deactivated successfully."
        )

class DepartmentViewSet(viewsets.ModelViewSet):
    """
    API endpoints for Department Management.
    """

    permission_classes = [RolePermission]

    permission_map = {
        "list": "department.view",
        "retrieve": "department.view",
        "create": "department.create",
        "update": "department.update",
        "partial_update": "department.update",
        "destroy": "department.delete",
    }

    queryset = Department.objects.filter(
        is_active=True
    ).order_by("name")

    serializer_class = DepartmentSerializer

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
        "description",
    )

    ordering_fields = (
        "name",
        "created_at",
    )

    ordering = (
        "name",
    )

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        department = DepartmentService.create_department(
            serializer.validated_data
        )

        response_serializer = self.get_serializer(
            department
        )

        return created_response(
            data=response_serializer.data,
            message="Department created successfully.",
        )

    def destroy(self, request, *args, **kwargs):

        department = self.get_object()

        DepartmentService.deactivate_department(
            department=department,
            user=request.user,
        )

        return success_response(
            message="Department deactivated successfully.",
        )
class DesignationViewSet(viewsets.ModelViewSet):
    """
    API endpoints for Designation Management.
    """

    permission_classes = [RolePermission]

    permission_map = {
        "list": "designation.view",
        "retrieve": "designation.view",
        "create": "designation.create",
        "update": "designation.update",
        "partial_update": "designation.update",
        "destroy": "designation.delete",
    }

    queryset = Designation.objects.filter(
        is_active=True
    ).order_by(
        "department",
        "hierarchy_level",
        "name",
    )

    serializer_class = DesignationSerializer

    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )

    filterset_fields = (
        "department",
        "is_active",
    )

    search_fields = (
        "name",
        "department__name",
    )

    ordering_fields = (
        "name",
        "hierarchy_level",
        "created_at",
    )

    ordering = (
        "department",
        "hierarchy_level",
        "name",
    )

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        designation = DesignationService.create_designation(
            serializer.validated_data
        )

        return created_response(
            data=DesignationSerializer(designation).data,
            message="Designation created successfully.",
        )

    def destroy(self, request, *args, **kwargs):

        designation = self.get_object()

        DesignationService.deactivate_designation(
            designation=designation,
            user=request.user,
        )

        return success_response(
            message="Designation deactivated successfully.",
        )


