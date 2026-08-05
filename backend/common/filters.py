class OrganizationFilterMixin:
    """
    Multi-tenant data isolation.

    Super Admin:
        Can see everything.

    Organization Owner:
        Can see only their organization.

    Branch Manager:
        Can see only their branch.
    """

    def get_queryset(self):

        queryset = super().get_queryset()

        user = self.request.user

        if user.is_superuser:
            return queryset

        if not hasattr(user, "employee_profile"):
            return queryset.none()

        employee = user.employee_profile

        role = employee.role.name if employee.role else None

        if role == "ORG_OWNER":
            return queryset.filter(
                organization=employee.organization
            )

        if role == "BRANCH_MANAGER":
            return queryset.filter(
                branch=employee.branch
            )

        return queryset.none()