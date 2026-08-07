from django.db import transaction

from audit.services import AuditService

from .models import (
    Organization,
    Branch,
    Department,
    Designation,
    Shift,
)


class OrganizationService:
    """
    Business logic for Organization Management.
    """

    @staticmethod
    @transaction.atomic
    def create_organization(validated_data):
        """
        Create a new organization.
        """

        organization = Organization.objects.create(
            **validated_data,
        )

        AuditService.log(
            user=None,
            action="CREATE",
            module="ORGANIZATION",
            object_id=str(organization.id),
            object_name=organization.name,
            description=(
                f"Organization '{organization.name}' created successfully."
            ),
        )

        return organization

    @staticmethod
    @transaction.atomic
    def deactivate_organization(organization, user=None):
        """
        Soft delete an organization by marking it inactive.
        """

        organization.is_active = False
        organization.save(update_fields=["is_active"])

        AuditService.log(
            user=user,
            action="DELETE",
            module="ORGANIZATION",
            object_id=str(organization.id),
            object_name=organization.name,
            description=(
                f"Organization '{organization.name}' deactivated successfully."
            ),
        )

        return organization


class BranchService:
    """
    Business logic for Branch Management.
    """

    @staticmethod
    @transaction.atomic
    def create_branch(validated_data):
        branch = Branch.objects.create(
            **validated_data,
        )

        AuditService.log(
            user=None,
            action="CREATE",
            module="BRANCH",
            object_id=str(branch.id),
            object_name=branch.name,
            description=(
                f"Branch '{branch.name}' created successfully."
            ),
        )

        return branch

    @staticmethod
    @transaction.atomic
    def deactivate_branch(branch, user=None):
        """
        Soft delete a branch.
        """

        branch.is_active = False
        branch.save(update_fields=["is_active"])

        AuditService.log(
            user=user,
            action="DELETE",
            module="BRANCH",
            object_id=str(branch.id),
            object_name=branch.name,
            description=(
                f"Branch '{branch.name}' deactivated successfully."
            ),
        )

        return branch 
    

class DepartmentService:
    """
    Business logic for Department Management.
    """

    @staticmethod
    @transaction.atomic
    def create_department(validated_data):

        department = Department.objects.create(
            **validated_data
        )

        AuditService.log(
            user=None,
            action="CREATE",
            module="DEPARTMENT",
            object_id=str(department.id),
            object_name=department.name,
            description=(
                f"Department '{department.name}' created successfully."
            ),
        )

        return department

    @staticmethod
    @transaction.atomic
    def deactivate_department(
        department,
        user=None,
    ):

        department.is_active = False

        department.save(
            update_fields=[
                "is_active",
            ]
        )

        AuditService.log(
            user=user,
            action="DELETE",
            module="DEPARTMENT",
            object_id=str(department.id),
            object_name=department.name,
            description=(
                f"Department '{department.name}' deactivated successfully."
            ),
        )

        return department


class DesignationService:
    """
    Business logic for Designation Management.
    """

    @staticmethod
    def create_designation(validated_data):

        designation = Designation.objects.create(
            **validated_data
        )

        AuditService.log(
            user=None,
            action="CREATE",
            module="DESIGNATION",
            object_id=str(designation.id),
            object_name=designation.name,
            description=f"Designation {designation.name} created successfully.",
        )

        return designation

    @staticmethod
    def deactivate_designation(
        designation,
        user,
    ):

        designation.is_active = False
        designation.save(
            update_fields=["is_active"]
        )

        AuditService.log(
            user=user,
            action="DELETE",
            module="DESIGNATION",
            object_id=str(designation.id),
            object_name=designation.name,
            description=f"Designation {designation.name} deactivated.",
        )

        return designation
    

class ShiftService:
    """
    Business logic for Shift Management.
    """

    @staticmethod
    def create_shift(validated_data):

        shift = Shift.objects.create(
            **validated_data
        )

        AuditService.log(
            user=None,
            action="CREATE",
            module="SHIFT",
            object_id=str(shift.id),
            object_name=shift.name,
            description=f"Shift {shift.name} created successfully.",
        )

        return shift

    @staticmethod
    def deactivate_shift(
        shift,
        user,
    ):

        shift.is_active = False

        shift.save(
            update_fields=[
                "is_active",
            ]
        )

        AuditService.log(
            user=user,
            action="DELETE",
            module="SHIFT",
            object_id=str(shift.id),
            object_name=shift.name,
            description=f"Shift {shift.name} deactivated.",
        )

        return shift
