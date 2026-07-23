from django.core.management.base import BaseCommand
from django.db import transaction

from employees.models import Employee
from trainers.models import Trainer, TrainerProfile


class Command(BaseCommand):
    help = "Migrate legacy Trainer records to Employee and TrainerProfile."

    def handle(self, *args, **options):
        self.stdout.write("")
        self.stdout.write("=" * 70)
        self.stdout.write(self.style.SUCCESS("FITFORGE TRAINER MIGRATION"))
        self.stdout.write("=" * 70)
        self.stdout.write("")

        trainer_count = Trainer.objects.count()

        self.stdout.write(f"Legacy Trainers Found : {trainer_count}")
        self.stdout.write("")

        self.stdout.write(
            self.style.WARNING(
                "Migration logic will be added in the next step."
            )
        )

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("Command executed successfully."))