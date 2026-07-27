from django.db import transaction

from audit.services import AuditService

from .models import Organization, Branch


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
        raise NotImplementedError(
            "Branch soft delete is not implemented yet."
        )   