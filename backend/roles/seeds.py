from roles.models import Permission

PERMISSIONS = [

    # Employee
    ("Employee", "employee.view", "View Employees"),
    ("Employee", "employee.create", "Create Employee"),
    ("Employee", "employee.update", "Update Employee"),
    ("Employee", "employee.delete", "Delete Employee"),

    # Trainer
    ("Trainer", "trainer.view", "View Trainers"),
    ("Trainer", "trainer.create", "Create Trainer"),
    ("Trainer", "trainer.update", "Update Trainer"),
    ("Trainer", "trainer.delete", "Delete Trainer"),

    # Members
    ("Member", "member.view", "View Members"),
    ("Member", "member.create", "Create Member"),
    ("Member", "member.update", "Update Member"),
    ("Member", "member.delete", "Delete Member"),

    # Attendance
    ("Attendance", "attendance.view", "View Attendance"),
    ("Attendance", "attendance.mark", "Mark Attendance"),
    ("Attendance", "attendance.update", "Update Attendance"),

    # Billing
    ("Billing", "billing.view", "View Billing"),
    ("Billing", "billing.create", "Create Payment"),
    ("Billing", "billing.refund", "Refund Payment"),

    # Membership
    ("Membership", "membership.view", "View Membership"),
    ("Membership", "membership.create", "Create Membership"),
    ("Membership", "membership.update", "Update Membership"),
    ("Membership", "membership.cancel", "Cancel Membership"),

    # Dashboard
    ("Dashboard", "dashboard.view", "View Dashboard"),

    # Reports
    ("Reports", "reports.view", "View Reports"),

    # Settings
    ("Settings", "settings.manage", "Manage Settings"),
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