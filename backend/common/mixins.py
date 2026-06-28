from rest_framework.exceptions import PermissionDenied

from .constants import ROLE_LEVELS


class RolePermissionMixin:
    """
    Enterprise RBAC Mixin

    Example:

    class EmployeeViewSet(
        RolePermissionMixin,
        ModelViewSet
    ):
        minimum_role_level = 80
    """

    minimum_role_level = 0

    def get_user_role_level(self):

        user = self.request.user

        if user.is_superuser:
            return ROLE_LEVELS["SUPER_ADMIN"]

        if (
            hasattr(user, "employee_profile")
            and user.employee_profile.role
        ):
            role_name = user.employee_profile.role.name

            return ROLE_LEVELS.get(role_name, 0)

        return 0

    def initial(self, request, *args, **kwargs):

        super().initial(request, *args, **kwargs)

        user_level = self.get_user_role_level()

        if user_level < self.minimum_role_level:
            raise PermissionDenied(
                "You do not have permission to perform this action."
            )