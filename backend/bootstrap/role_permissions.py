from roles.models import Role, Permission
from common.role_codes import RoleCodes


ROLE_PERMISSION_MAP = {
    "SUPER_ADMIN": "__ALL__",

    "ORG_OWNER": [
        "dashboard.view",
        "employee.view",
        "employee.create",
        "employee.update",
        "trainer.view",
        "trainer.create",
        "trainer.update",
        "member.view",
        "member.create",
        "member.update",
        "attendance.view",
        "attendance.mark",
        "billing.view",
        "billing.create",
        "membership.view",
        "membership.create",
        "membership.update",
        "reports.view",
    ],

    "BRANCH_MANAGER": [
        "dashboard.view",
        "employee.view",
        "employee.create",
        "employee.update",
        "trainer.view",
        "trainer.create",
        "trainer.update",
        "member.view",
        "member.create",
        "attendance.view",
        "attendance.mark",
        "membership.view",
        "billing.view",
    ],

    "HR": [
        "employee.view",
        "employee.create",
        "employee.update",
    ],

    "OPERATIONS_MANAGER": [
        "dashboard.view",
        "trainer.view",
        "attendance.view",
        "attendance.mark",
    ],

    "FITNESS_CONSULTANT": [
        "member.view",
        "member.create",
        "membership.view",
    ],

    "SALES_EXECUTIVE": [
        "member.view",
        "member.create",
        "membership.view",
        "membership.create",
        "billing.create",
    ],

    "RECEPTIONIST": [
        "member.view",
        "attendance.view",
    ],

    "TRAINER": [
        "member.view",
        "attendance.mark",
    ],

    "FREELANCE_TRAINER": [
        "member.view",
        "attendance.mark",
    ],

    "NUTRITIONIST": [
        "member.view",
    ],

    "HOUSEKEEPING": [],

    "MEMBER": [],

    "ONLINE_MEMBER": [],
}


def assign_default_permissions():
    assigned_roles = 0

    for role_name, permission_codes in ROLE_PERMISSION_MAP.items():

        role = Role.objects.filter(code=role_name).first()

        if not role:
            print(f"⚠️ Role '{role_name}' not found. Skipping...")
            continue

        if permission_codes == "__ALL__":
            role.permissions.set(Permission.objects.all())
        else:
            permissions = Permission.objects.filter(
                code__in=permission_codes
            )
            role.permissions.set(permissions)

        assigned_roles += 1

    return assigned_roles
