from django.db import transaction

from rest_framework.exceptions import ValidationError

from .service import BootstrapService

from roles.models import Role
from common.role_codes import RoleCodes

from core.models import Organization
from core.services import OrganizationService, BranchService

from employees.services import EmployeeService



class BootstrapSuperAdminService:
    """
    Creates the first Super Admin for a fresh FitForge installation.

    Safe to run multiple times.
    """

    @staticmethod
    @transaction.atomic
    def run(validated_data):
        """
        Performs the initial FitForge installation.
        """

        # Prevent multiple installations
        if Organization.objects.exists():
            raise ValidationError(
                {
                    "message": "FitForge has already been installed."
                }
            )

        # Seed permissions and roles
        BootstrapService.run()

        # ----------------------------------------
        # Create Organization
        # ----------------------------------------

        organization = OrganizationService.create_organization(
           validated_data["organization"]
        )

        # ----------------------------------------
        # Create Primary Branch
        # ----------------------------------------

        branch_data = validated_data["branch"]
        branch_data["organization"] = organization

        branch = BranchService.create_branch(
            branch_data
        )

        # ----------------------------------------
        # Get Super Admin Role
        # ----------------------------------------

        super_admin_role = Role.objects.get(
            code=RoleCodes.SUPER_ADMIN
        )

        # ----------------------------------------
        # Create Super Admin Employee
        # ----------------------------------------

        admin_data = validated_data["admin"]

        admin_data["organization"] = organization
        admin_data["branch"] = branch
        admin_data["employee_classification"] = "ADMIN"

        employee_result = EmployeeService.create_employee(
            validated_data=admin_data,
            role=super_admin_role,
        )

        return {
            "organization": organization,
            "branch": branch,
            "employee": employee_result["employee"],
            "employee_code": employee_result["employee"].employee_code,
            "temporary_password": employee_result["temporary_password"],
        }
   