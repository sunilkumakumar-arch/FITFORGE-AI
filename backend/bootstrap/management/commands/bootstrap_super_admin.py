from django.core.management.base import BaseCommand

from bootstrap.super_admin_service import BootstrapSuperAdminService


class Command(BaseCommand):
    help = "Create the initial Super Admin for FitForge."

    def handle(self, *args, **options):

        self.stdout.write("")
        self.stdout.write("=" * 60)
        self.stdout.write(" FitForge Super Admin Bootstrap")
        self.stdout.write("=" * 60)

        result = BootstrapSuperAdminService.run()

        self.stdout.write("")

        if result["created"]:

            self.stdout.write(
                self.style.SUCCESS(
                    "Super Admin created successfully."
                )
            )

            self.stdout.write(
                f"Employee Code : {result['employee_code']}"
            )

            self.stdout.write(
                f"Username      : {result['username']}"
            )

            self.stdout.write(
                f"Password      : {result['temporary_password']}"
            )

        else:

            self.stdout.write(
                self.style.WARNING(
                    "Super Admin already exists."
                )
            )

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                "Bootstrap completed successfully."
            )
        )