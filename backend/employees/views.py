from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import Employee
from .serializers import EmployeeSerializer
from .services import EmployeeService
from .permissions import EmployeePermission
from common.mixins import RolePermissionMixin
from common.filters import OrganizationFilterMixin
from common.constants import ROLE_LEVELS
from common.role_codes import RoleCodes
from roles.permissions import RolePermission

class EmployeeViewSet(
    OrganizationFilterMixin,
    RolePermissionMixin,
    viewsets.ModelViewSet,
):
    
    permission_classes = [RolePermission]

    minimum_role_level = ROLE_LEVELS[RoleCodes.BRANCH_MANAGER]

    required_permission = "employee.create"
    """
    API endpoints for Employee Management.
    """

    queryset = Employee.objects.all().order_by("employee_code")
    serializer_class = EmployeeSerializer
    

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = EmployeeService.create_employee(
            serializer.validated_data
        )

        employee = result["employee"]
        temporary_password = result["temporary_password"]

        response_serializer = self.get_serializer(employee)

        return Response(
            {
                "message": "Employee created successfully.",
                "employee": response_serializer.data,
                "login_credentials": {
                    "username": employee.user.username,
                    "temporary_password": temporary_password,
                },
            },
            status=status.HTTP_201_CREATED,
        )
