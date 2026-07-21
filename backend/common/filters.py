class OrganizationFilterMixin:
    """
    Multi-tenant data isolation.

    RBAC decides IF a user can access a module.
    This mixin decides WHICH records they can see.
    """

    def get_queryset(self):

        queryset = super().get_queryset()

        user = self.request.user

        if user.is_superuser:
            return queryset

        if not hasattr(user, "employee_profile"):
            return queryset.none()

        employee = user.employee_profile

        if not employee.organization:
            return queryset.none()

        role = employee.role.name if employee.role else None

        # Organization-wide access
        organization_roles = {
            "ORG_OWNER",
            "HR",
            "OPERATIONS_MANAGER",
        }

        if role in organization_roles:
            return queryset.filter(
                organization=employee.organization
            )

        # Branch-only access
        branch_roles = {
            "BRANCH_MANAGER",
        }

        if role in branch_roles:
            return queryset.filter(
                branch=employee.branch
            )

        return queryset.none()