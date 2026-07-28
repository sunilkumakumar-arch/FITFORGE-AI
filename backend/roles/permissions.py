from rest_framework.permissions import BasePermission
from employees.models import Employee

import logging

logger = logging.getLogger(__name__)

class RolePermission(BasePermission):

    message = "You do not have permission to perform this action."

    def has_permission(self, request, view):

        logger.warning("=" * 60)
        logger.warning("RolePermission is being executed")

        permission_map = getattr(view, "permission_map", None)

        if permission_map:
            required_permission = permission_map.get(view.action)
        else:
            required_permission = getattr(view, "required_permission", None)

        logger.warning(f"Action: {getattr(view, 'action', None)}")
        logger.warning(f"Required Permission: {required_permission}")

        if required_permission is None:
            return request.user.is_authenticated

        if not request.user.is_authenticated:
            logger.warning("User is not authenticated")
            return False

        try:
            employee = (
                Employee.objects
                .select_related("role")
                .prefetch_related("role__permissions")
                .get(user=request.user)
            )
        except Employee.DoesNotExist:
            logger.warning("Employee not found")
            return False

        logger.warning(f"Employee: {employee.employee_code}")
        logger.warning(f"Employment Status: {employee.employment_status}")
        logger.warning(f"Role: {employee.role.code if employee.role else None}")
        logger.warning(f"Role Active: {employee.role.is_active if employee.role else None}")

        if employee.employment_status != "ACTIVE":
            logger.warning("Employment status check failed")
            return False

        if employee.role is None:
            logger.warning("Role is None")
            return False

        if not employee.role.is_active:
            logger.warning("Role is inactive")
            return False

        if employee.role.code == "SUPER_ADMIN":
            logger.warning("SUPER_ADMIN bypass")
            return True

        has_perm = employee.role.permissions.filter(
            code=required_permission,
            is_active=True,
        ).exists()

        logger.warning(f"Permission Exists: {has_perm}")

        return has_perm