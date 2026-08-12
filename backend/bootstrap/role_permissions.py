from roles.models import Role, Permission
from common.role_codes import RoleCodes


ROLE_PERMISSION_MAP = {
    "SUPER_ADMIN": "__ALL__",

    "ORG_OWNER": [
        "dashboard.view",

        "employee.view",
        "employee.create",
        "employee.update",
        "employee.delete",

        "trainer.view",
        "trainer.create",
        "trainer.update",
        "trainer.delete",

        "member.view",
        "member.create",
        "member.update",
        "member.delete",

        "attendance.view",
        "attendance.mark",
        "attendance.update",
        "attendance.delete",

        "billing.view",
        "billing.create",
        "billing.update",
        "billing.delete",
        "billing.refund",

        "membership.view",
        "membership.create",
        "membership.update",
        "membership.delete",
        "membership.cancel",

        "workout.view",
        "workout.create",
        "workout.update",
        "workout.delete",

        "nutrition.view",
        "nutrition.create",
        "nutrition.update",

        "ai_coach.use",

        "reports.view",
        "settings.manage",

        "gym_management.view",
        "gym_management.create",
        "gym_management.update",
        "gym_management.delete",

        
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
        "member.update",

        "attendance.view",
        "attendance.mark",
        "attendance.update",

        "billing.view",
        "billing.create",
        "billing.update",

        "membership.view",
        "membership.create",
        "membership.update",

        "workout.view",
        "workout.create",
        "workout.update",

        "nutrition.view",

        "reports.view",

        "gym_management.view",
        "gym_management.create",
        "gym_management.update",
        "gym_management.delete",
    ],

    "HR": [
        "employee.view",
        "employee.create",
        "employee.update",
        "employee.delete",
    ],

    "OPERATIONS_MANAGER": [
        "dashboard.view",

        "trainer.view",
        "trainer.update",

        "attendance.view",
        "attendance.mark",
        "attendance.update",

        "workout.view",
        "workout.update",

        "reports.view",
    ],

    "FITNESS_CONSULTANT": [
        "member.view",
        "member.create",

        "membership.view",
        "membership.create",

        "workout.view",

        "nutrition.view",
    ],

    "SALES_EXECUTIVE": [
        "member.view",
        "member.create",

        "membership.view",
        "membership.create",

        "billing.create",
        "billing.view",
    ],

    "RECEPTIONIST": [
        "member.view",

        "attendance.view",
        "attendance.mark",

        "membership.view",

        "billing.view",
        "billing.create",
    ],

    "TRAINER": [
        "member.view",

        "attendance.mark",

        "workout.view",
        "workout.update",

        "nutrition.view",

        "ai_coach.use",
    ],

    "FREELANCE_TRAINER": [
        "member.view",

        "attendance.mark",

        "workout.view",

        "nutrition.view",
    ],

    "NUTRITIONIST": [
        "member.view",

        "nutrition.view",
        "nutrition.create",
        "nutrition.update",
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