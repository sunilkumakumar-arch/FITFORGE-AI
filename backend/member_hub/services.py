from django.db import transaction
from django.db.models import Max

from .models import MemberHub
from .qr import QRService


class MemberHubService:

    PUBLIC_PREFIX = "FFX26"

    @staticmethod
    def _get_next_sequence():
        """
        Returns the next sequential member number.
        """

        max_id = MemberHub.objects.aggregate(
            max_id=Max("id")
        )["max_id"]

        return (max_id or 0) + 1

    @classmethod
    def _generate_public_member_id(cls):
        """
        Generates a public member ID.

        Example:
            FFX26-000001
        """

        sequence = cls._get_next_sequence()

        return f"{cls.PUBLIC_PREFIX}-{sequence:06d}"

    @classmethod
    @transaction.atomic
    def create_for_member(cls, member):
        """
        Creates a MemberHub if one does not already exist.
        Automatically generates the QR image.
        """

        hub, created = MemberHub.objects.get_or_create(
            member=member,
            defaults={
                "public_member_id": cls._generate_public_member_id(),
            },
        )

        if created:
            QRService.save_qr_image(hub)

        return hub

    @classmethod
    @transaction.atomic
    def regenerate_qr(cls, hub):
        """
        Regenerates the QR image for an existing member.
        """

        return QRService.regenerate_qr(hub)