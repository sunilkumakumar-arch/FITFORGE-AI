from rest_framework.exceptions import PermissionDenied

from .constants import ROLE_LEVELS


class RolePermissionMixin:
    """
    Enterprise RBAC Mixin

    Responsibilities:
    - Enforce minimum role hierarchy
    - Enforce permission-based authorization
    """

    minimum_role_level = 0
    required_permission = None

    def get_employee(self):
        return getattr(self.request.user, "employee_profile", None)

    def get_user_role_level(self):
        user = self.request.user

        if user.is_superuser:
            return ROLE_LEVELS["SUPER_ADMIN"]

        employee = self.get_employee()

        if employee and employee.role:
            return ROLE_LEVELS.get(employee.role.name, 0)

        return 0

    def has_required_permission(self):
        if not self.required_permission:
            return True

        employee = self.get_employee()

        if not employee or not employee.role:
            return False

        return employee.role.permissions.filter(
            code=self.required_permission,
            is_active=True,
        ).exists()

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)

        if self.get_user_role_level() < self.minimum_role_level:
            raise PermissionDenied(
                "You do not have the required role level."
            )

        if not self.has_required_permission():
            raise PermissionDenied(
                "You do not have the required permission."
            )