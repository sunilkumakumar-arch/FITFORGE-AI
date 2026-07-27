from common.role_codes import RoleCodes

"""
FitForge Role Hierarchy

Higher number = Higher authority
"""

ROLE_LEVELS = {
    RoleCodes.SUPER_ADMIN: 100,
    RoleCodes.ORG_OWNER: 90,
    RoleCodes.BRANCH_MANAGER: 80,
    RoleCodes.HR: 70,
    RoleCodes.OPERATIONS_MANAGER: 60,
    RoleCodes.FITNESS_CONSULTANT: 50,
    RoleCodes.SALES_EXECUTIVE: 45,
    RoleCodes.RECEPTIONIST: 40,
    RoleCodes.TRAINER: 30,
    RoleCodes.FREELANCE_TRAINER: 25,
    RoleCodes.MEMBER: 10,
    RoleCodes.ONLINE_MEMBER: 5,
}