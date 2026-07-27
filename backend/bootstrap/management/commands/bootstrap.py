from django.core.management.base import BaseCommand

from bootstrap.service import BootstrapService


class Command(BaseCommand):
    help = "Initialize FitForge master data."

    def handle(self, *args, **options):

        self.stdout.write("")
        self.stdout.write("=" * 60)
        self.stdout.write(" FitForge Bootstrap")
        self.stdout.write("=" * 60)

        result = BootstrapService.run()

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                f"Permissions Created : {result['permissions_created']}"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Roles Created : {result['roles_created']}"
            )
        )

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS("Bootstrap completed successfully.")
        )