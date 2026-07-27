from django.db import transaction

from roles.seeds import seed_permissions
from bootstrap.roles import seed_roles
from bootstrap.role_permissions import assign_default_permissions

from core.models import Organization
from core.services import OrganizationService, BranchService

from employees.services import EmployeeService
from roles.models import Role


class BootstrapService:
    """
    Initializes FitForge master data.
    Safe to run multiple times.
    """

    @staticmethod
    @transaction.atomic
    def run():

        result = {}

        created_permissions = seed_permissions()
        created_roles = seed_roles()

        assigned_roles = assign_default_permissions()

        result["permissions_created"] = created_permissions
        result["roles_created"] = created_roles
        result["roles_configured"] = assigned_roles

        return result


class BootstrapSuperAdminService:
    """
    Installs FitForge for the first time.

    Creates:
    - Organization
    - Primary Branch
    - Super Admin Employee

    This service can only run once.
    """

    @staticmethod
    @transaction.atomic
    def run(validated_data):
        pass    
    

    