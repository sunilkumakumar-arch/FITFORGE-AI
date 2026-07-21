from django.core.management.base import BaseCommand

from roles.seeds import seed_permissions


class Command(BaseCommand):

    help = "Seed FitForge permissions"

    def handle(self, *args, **kwargs):

        count = seed_permissions()

        self.stdout.write(
            self.style.SUCCESS(
                f"{count} permissions created successfully."
            )
        )