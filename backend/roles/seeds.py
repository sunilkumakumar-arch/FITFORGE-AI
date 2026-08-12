from roles.models import Permission

PERMISSIONS = [

    # ==========================
    # Employee
    # ==========================
    ("Employee", "employee.view", "View Employees"),
    ("Employee", "employee.create", "Create Employee"),
    ("Employee", "employee.update", "Update Employee"),
    ("Employee", "employee.delete", "Delete Employee"),

    # ==========================
    # Trainer
    # ==========================
    ("Trainer", "trainer.view", "View Trainers"),
    ("Trainer", "trainer.create", "Create Trainer"),
    ("Trainer", "trainer.update", "Update Trainer"),
    ("Trainer", "trainer.delete", "Delete Trainer"),

    # ==========================
    # Member
    # ==========================
    ("Member", "member.view", "View Members"),
    ("Member", "member.create", "Create Member"),
    ("Member", "member.update", "Update Member"),
    ("Member", "member.delete", "Delete Member"),

    # ==========================
    # Membership
    # ==========================
    ("Membership", "membership.view", "View Membership"),
    ("Membership", "membership.create", "Create Membership"),
    ("Membership", "membership.update", "Update Membership"),
    ("Membership", "membership.delete", "Delete Membership"),
    ("Membership", "membership.cancel", "Cancel Membership"),

    # ==========================
    # Billing
    # ==========================
    ("Billing", "billing.view", "View Billing"),
    ("Billing", "billing.create", "Create Payment"),
    ("Billing", "billing.update", "Update Payment"),
    ("Billing", "billing.delete", "Delete Payment"),
    ("Billing", "billing.refund", "Refund Payment"),

    # ==========================
    # Attendance
    # ==========================
    ("Attendance", "attendance.view", "View Attendance"),
    ("Attendance", "attendance.mark", "Mark Attendance"),
    ("Attendance", "attendance.update", "Update Attendance"),
    ("Attendance", "attendance.delete", "Delete Attendance"),

    # ==========================
    # Workout
    # ==========================
    ("Workout", "workout.view", "View Workout"),
    ("Workout", "workout.create", "Create Workout"),
    ("Workout", "workout.update", "Update Workout"),
    ("Workout", "workout.delete", "Delete Workout"),

    # ==========================
    # Nutrition
    # ==========================
    ("Nutrition", "nutrition.view", "View Nutrition"),
    ("Nutrition", "nutrition.create", "Create Nutrition"),
    ("Nutrition", "nutrition.update", "Update Nutrition"),
    ("Nutrition", "nutrition.delete", "Delete Nutrition"),

    # ==========================
    # AI Coach
    # ==========================
    ("AI Coach", "ai_coach.use", "Use AI Coach"),

    # ==========================
    # Dashboard
    # ==========================
    ("Dashboard", "dashboard.view", "View Dashboard"),

    # ==========================
    # Reports
    # ==========================
    ("Reports", "reports.view", "View Reports"),

    # ==========================
    # Settings
    # ==========================
    ("Settings", "settings.manage", "Manage Settings"),

    # ==========================
    # Gym Management
    # ==========================
    ("Gym Management", "gym_management.view", "View Gym Management"),
    ("Gym Management", "gym_management.create", "Create Gym Management"),
    ("Gym Management", "gym_management.update", "Update Gym Management"),
    ("Gym Management", "gym_management.delete", "Delete Gym Management"),
]


def seed_permissions():

    created = 0

    for module, code, name in PERMISSIONS:

        _, is_created = Permission.objects.get_or_create(
            code=code,
            defaults={
                "module": module,
                "name": name,
            },
        )

        if is_created:
            created += 1

    return created