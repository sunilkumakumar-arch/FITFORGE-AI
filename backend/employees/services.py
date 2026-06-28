from django.db import transaction

from .models import Employee
from audit.services import AuditService


class EmployeeService:
    """
    Business logic for Employee Management.
    """

    @staticmethod
    def generate_employee_code():
        last_employee = (
            Employee.objects
            .order_by("-id")
            .first()
        )

        if not last_employee:
            return "EMP000001"

        last_number = int(
            last_employee.employee_code.replace("EMP", "")
        )

        next_number = last_number + 1

        return f"EMP{next_number:06d}"

    @staticmethod
    @transaction.atomic
    def create_employee(validated_data):

        employee = Employee.objects.create(
            **validated_data
        )

        AuditService.log(
            user=None,
            action="CREATE",
            module="EMPLOYEE",
            object_id=str(employee.id),
            object_name=employee.employee_code,
            description=f"Employee {employee.employee_code} created successfully",
        )

        return employee