import secrets
import string

from django.contrib.auth import get_user_model
from django.db import transaction

from audit.services import AuditService
from .models import Employee

User = get_user_model()


class EmployeeService:
    """
    Business logic for Employee Management.
    """

    @staticmethod
    def generate_temporary_password(length=12):
            """
            Generate a secure temporary password for new employees.
            """

            alphabet = (
                string.ascii_letters +
                string.digits +
                "!@#$%^&*"
            )

            while True:
                password = "".join(
                    secrets.choice(alphabet)
                    for _ in range(length)
                )

                if (
                    any(c.islower() for c in password)
                    and any(c.isupper() for c in password)
                    and any(c.isdigit() for c in password)
                    and any(c in "!@#$%^&*" for c in password)
                ):
                    return password


    @staticmethod
    def create_login_account(
        employee_code,
        first_name,
        last_name,
        email,
    ):
        """
        Create the Django login account for a new employee.
        """

        if User.objects.filter(username=employee_code).exists():
            raise ValueError(
                f"Username '{employee_code}' already exists."
            )

        temporary_password = EmployeeService.generate_temporary_password()

        user = User.objects.create_user(
            username=employee_code,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=temporary_password,
        )

        return user, temporary_password              

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

        employee_code = EmployeeService.generate_employee_code()

        print("=" * 60)
        print("Generated Employee Code :", employee_code)
        print("Validated Data :", validated_data)
        print("=" * 60)
        

        user, temporary_password = EmployeeService.create_login_account(
            employee_code=employee_code,
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=validated_data["email"],
        )
        print("Saved Employee Code :", employee.employee_code)

        employee = Employee.objects.create(
            user=user,
            employee_code=employee_code,
            **validated_data,
        )

        AuditService.log(
            user=user,
            action="CREATE",
            module="EMPLOYEE",
            object_id=str(employee.id),
            object_name=employee.employee_code,
            description=f"Employee {employee.employee_code} created successfully",
        )

        return {
            "employee": employee,
            "temporary_password": temporary_password,
        }