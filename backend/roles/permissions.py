from rest_framework.permissions import BasePermission
from .models import UserRole


class IsSuperAdmin(BasePermission):

    def has_permission(self, request, view):
        try:
            return (
                request.user.is_authenticated
                and request.user.role_assignment.role.name
                == "SUPER_ADMIN"
            )
        except:
            return False


class IsManager(BasePermission):

    def has_permission(self, request, view):
        try:
            return (
                request.user.is_authenticated
                and request.user.role_assignment.role.name
                == "MANAGER"
            )
        except:
            return False


class IsTrainer(BasePermission):

    def has_permission(self, request, view):
        try:
            return (
                request.user.is_authenticated
                and request.user.role_assignment.role.name
                == "TRAINER"
            )
        except:
            return False


class IsReceptionist(BasePermission):

    def has_permission(self, request, view):
        try:
            return (
                request.user.is_authenticated
                and request.user.role_assignment.role.name
                == "RECEPTIONIST"
            )
        except:
            return False


class IsMember(BasePermission):

    def has_permission(self, request, view):
        try:
            return (
                request.user.is_authenticated
                and request.user.role_assignment.role.name
                == "MEMBER"
            )
        except:
            return False
        
     

class IsAdminOrManager(BasePermission):

    def has_permission(self, request, view):

        try:
            role = request.user.role_assignment.role.name

            return role in [
                "SUPER_ADMIN",
                "MANAGER"
            ]

        except:
            return False           


from employees.models import Employee


class RolePermission(BasePermission):

    message = "You do not have permission to perform this action."

    def has_permission(self, request, view):

        required_permission = getattr(
            view,
            "required_permission",
            None,
        )

        # If the view doesn't require a permission,
        # allow authenticated users.
        if required_permission is None:
            return True

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