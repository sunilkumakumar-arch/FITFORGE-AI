from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import Employee
from .serializers import EmployeeSerializer
from .services import EmployeeService
from .permissions import EmployeePermission
from common.mixins import RolePermissionMixin
from common.filters import OrganizationFilterMixin

class EmployeeViewSet(
    OrganizationFilterMixin,
    RolePermissionMixin,
    viewsets.ModelViewSet,
):
    
    minimum_role_level = 80
    """
    API endpoints for Employee Management.
    """

    queryset = Employee.objects.all().order_by("employee_code")
    serializer_class = EmployeeSerializer
    permission_classes = [EmployeePermission]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        employee = EmployeeService.create_employee(
            serializer.validated_data
        )

        response_serializer = self.get_serializer(employee)

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )
