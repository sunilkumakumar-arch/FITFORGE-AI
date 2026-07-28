from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import Employee
from .serializers import EmployeeSerializer
from .services import EmployeeService

from common.filters import OrganizationFilterMixin

from roles.permissions import RolePermission

class EmployeeViewSet(
    OrganizationFilterMixin,
    viewsets.ModelViewSet,
):
    
    

    permission_classes = [RolePermission]


    permission_map = {
        "list": "employee.view",
        "retrieve": "employee.view",
        "create": "employee.create",
        "update": "employee.edit",
        "partial_update": "employee.edit",
        "destroy": "employee.delete",
    }
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
