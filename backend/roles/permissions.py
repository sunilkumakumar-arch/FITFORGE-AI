from rest_framework.permissions import BasePermission
from employees.models import Employee

class RolePermission(BasePermission):

    message = "You do not have permission to perform this action."

    def has_permission(self, request, view):

        permission_map = getattr(
            view,
            "permission_map",
            None,
        )

        if permission_map:
            required_permission = permission_map.get(view.action)
        else:
            required_permission = getattr(
                view,
                "required_permission",
                None,
            )

        # If the view doesn't require a permission,
        # allow authenticated users.
        if required_permission is None:
            return request.user.is_authenticated

        if not request.user.is_authenticated:
            return False

        try:

            employee = (
                Employee.objects
                .select_related("role")
                .prefetch_related("role__permissions")
                .get(user=request.user)
            )

        except Employee.DoesNotExist:
            return False

        if employee.role is None:
            return False

        return employee.role.permissions.filter(
            code=required_permission,
            is_active=True,
        ).exists()