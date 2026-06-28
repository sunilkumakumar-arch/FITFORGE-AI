from rest_framework.permissions import BasePermission


class IsSuperAdmin(BasePermission):
    """
    Allows access only to Super Admin users.
    """

    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False

        if user.is_superuser:
            return True

        if hasattr(user, "employee_profile") and user.employee_profile.role:
            return (
                user.employee_profile.role.name == "SUPER_ADMIN"
            )

        return False


class IsOrganizationOwner(BasePermission):
    """
    Allows access only to Organization Owners.
    """

    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False

        if hasattr(user, "employee_profile") and user.employee_profile.role:
            return (
                user.employee_profile.role.name == "ORG_OWNER"
            )

        return False


class IsBranchManager(BasePermission):
    """
    Allows access only to Branch Managers.
    """

    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False

        if hasattr(user, "employee_profile") and user.employee_profile.role:
            return (
                user.employee_profile.role.name == "BRANCH_MANAGER"
            )

        return False


class IsTrainer(BasePermission):
    """
    Allows access only to Trainers.
    """

    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False

        if hasattr(user, "employee_profile") and user.employee_profile.role:
            return (
                user.employee_profile.role.name in [
                    "TRAINER",
                    "FREELANCE_TRAINER",
                ]
            )

        return False


class IsReceptionist(BasePermission):
    """
    Allows access only to Receptionists.
    """

    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False

        if hasattr(user, "employee_profile") and user.employee_profile.role:
            return (
                user.employee_profile.role.name == "RECEPTIONIST"
            )

        return False


class IsEmployee(BasePermission):
    """
    Allows any authenticated employee.
    """

    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False

        return hasattr(user, "employee_profile")