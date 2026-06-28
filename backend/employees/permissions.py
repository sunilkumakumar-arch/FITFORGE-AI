from rest_framework.permissions import BasePermission


class EmployeePermission(BasePermission):
    """
    Permission class for Employee APIs.
    """

    ALLOWED_ROLES = {
        "SUPER_ADMIN",
        "ORG_OWNER",
        "BRANCH_MANAGER",
    }

    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        if not hasattr(request.user, "employee_profile"):
            return False

        employee = request.user.employee_profile

        if employee.role is None:
            return False

        if not employee.role.is_active:
            return False

        return employee.role.name in self.ALLOWED_ROLES