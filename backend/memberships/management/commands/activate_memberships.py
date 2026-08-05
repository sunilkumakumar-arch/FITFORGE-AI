from django.core.management.base import BaseCommand
from django.utils import timezone

from memberships.models import MemberMembership


class Command(BaseCommand):
    help = "Activate scheduled memberships."

    def handle(self, *args, **options):

        today = timezone.now().date()

        scheduled_memberships = (
            MemberMembership.objects.filter(
                status="Scheduled",
                start_date=today,
            )
        )

        activated = 0

        for membership in scheduled_memberships:

            (
                MemberMembership.objects.filter(
                    member=membership.member,
                    status="Active",
                )
                .exclude(id=membership.id)
                .update(status="Expired")
            )

            membership.status = "Active"
            membership.save(update_fields=["status"])

            activated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"{activated} memberships activated."
            )
        )