from roles.models import Role
from common.role_codes import RoleCodes

DEFAULT_ROLES = [
    {
        "code": RoleCodes.SUPER_ADMIN,
        "name": "Super Admin",
        "description": "Complete system access",
        "is_system_role": True,
    },
    {
        "code": RoleCodes.ORG_OWNER,
        "name": "Organization Owner",
        "description": "Owns and manages the organization",
        "is_system_role": True,
    },
    {
        "code": RoleCodes.BRANCH_MANAGER,
        "name": "Branch Manager",
        "description": "Manages a gym branch",
        "is_system_role": True,
    },
    {
        "code": RoleCodes.HR,
        "name": "Human Resources",
        "description": "Human resource management",
        "is_system_role": True,
    },
    {
        "code": RoleCodes.OPERATIONS_MANAGER,
        "name": "Operations Manager",
        "description": "Operations management",
        "is_system_role": True,
    },
    {
        "code": RoleCodes.FITNESS_CONSULTANT,
        "name": "Fitness Consultant",
        "description": "Fitness consultation",
        "is_system_role": True,
    },
    {
        "code": RoleCodes.SALES_EXECUTIVE,
        "name": "Sales Executive",
        "description": "Membership sales",
        "is_system_role": True,
    },
    {
        "code": RoleCodes.RECEPTIONIST,
        "name": "Receptionist",
        "description": "Front desk operations",
        "is_system_role": True,
    },
    {
        "code": RoleCodes.TRAINER,
        "name": "Trainer",
        "description": "Personal trainer",
        "is_system_role": True,
    },
    {
        "code": RoleCodes.FREELANCE_TRAINER,
        "name": "Freelance Trainer",
        "description": "Freelance trainer",
        "is_system_role": True,
    },
    {
        "code": RoleCodes.NUTRITIONIST,
        "name": "Nutritionist",
        "description": "Nutrition planning",
        "is_system_role": True,
    },
    {
        "code": RoleCodes.HOUSEKEEPING,
        "name": "Housekeeping",
        "description": "Housekeeping staff",
        "is_system_role": True,
    },
    {
        "code": RoleCodes.MEMBER,
        "name": "Member",
        "description": "Gym member",
        "is_system_role": True,
    },
    {
        "code": RoleCodes.ONLINE_MEMBER,
        "name": "Online Member",
        "description": "Online member",
        "is_system_role": True,
    },
]

def seed_roles():
    created = 0

    for role in DEFAULT_ROLES:
        _, is_created = Role.objects.get_or_create(
            code=role["code"],
            defaults=role,
        )

        if is_created:
            created += 1

    return created