from django.core.management.base import BaseCommand

from certifications.models import Certification




CERTIFICATIONS = [

    ("ACE Certified Personal Trainer", "ACE"),
    ("ACE Sports Nutrition Specialist", "ACE"),
    ("ACE Orthopedic Exercise Specialist", "ACE"),
    ("ACE Medical Exercise Specialist", "ACE"),

    ("NASM Certified Personal Trainer", "NASM"),
    ("NASM Corrective Exercise Specialist", "NASM"),
    ("NASM Performance Enhancement Specialist", "NASM"),
    ("NASM Nutrition Coach", "NASM"),

    ("ACSM Certified Personal Trainer", "ACSM"),
    ("ACSM Exercise Physiologist", "ACSM"),

    ("NSCA Certified Strength and Conditioning Specialist", "NSCA"),
    ("NSCA Certified Personal Trainer", "NSCA"),

    ("ISSA Certified Personal Trainer", "ISSA"),
    ("ISSA Nutritionist", "ISSA"),
    ("ISSA Strength and Conditioning Coach", "ISSA"),

    ("CrossFit Level 1", "CrossFit"),
    ("CrossFit Level 2", "CrossFit"),

    ("TRX Suspension Trainer", "TRX"),

    ("Functional Training Specialist", "General"),

    ("Corrective Exercise Specialist", "General"),

    ("Sports Performance Coach", "General"),

    ("Strength and Conditioning Coach", "General"),

    ("Powerlifting Coach", "General"),

    ("Olympic Weightlifting Coach", "General"),

    ("Kettlebell Instructor", "General"),

    ("Mobility Specialist", "General"),

    ("Yoga Alliance RYT 200", "Yoga Alliance"),

    ("Pilates Instructor", "Pilates"),

    ("Pre and Post Natal Fitness Specialist", "General"),

    ("Senior Fitness Specialist", "General"),

    ("Kids Fitness Specialist", "General"),

    ("CPR Certified", "Red Cross"),

    ("AED Certified", "Red Cross"),

    ("First Aid Certified", "Red Cross"),
]


class Command(BaseCommand):

    help = "Seed certifications"

    def handle(self, *args, **kwargs):

        count = 0

        for name, organization in CERTIFICATIONS:

            _, created = Certification.objects.get_or_create(
                name=name,
                defaults={
                    "issuing_organization": organization,
                    "is_active": True,
                },
            )

            if created:
                count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"{count} certifications inserted successfully."
            )
        )