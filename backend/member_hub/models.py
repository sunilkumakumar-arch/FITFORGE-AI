import uuid

from django.db import models
from accounts.models import Member


class MemberHub(models.Model):

    FORGE = "FORGE"
    IRON = "IRON"
    STEEL = "STEEL"
    TITAN = "TITAN"
    BEAST = "BEAST"
    LEGEND = "LEGEND"
    ELITE = "ELITE"

    CARD_LEVELS = [
        (FORGE, "Forge"),
        (IRON, "Iron"),
        (STEEL, "Steel"),
        (TITAN, "Titan"),
        (BEAST, "Beast"),
        (LEGEND, "Legend"),
        (ELITE, "Elite"),
    ]

    member = models.OneToOneField(
        Member,
        on_delete=models.CASCADE,
        related_name="hub",
    )

    public_member_id = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
        blank=True,
        default="",
    )

    card_level = models.CharField(
        max_length=20,
        choices=CARD_LEVELS,
        default=FORGE,
    )
    card_version = models.PositiveSmallIntegerField(
        default=1,
    )

    

    qr_token = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )

    qr_code = models.ImageField(
        upload_to="member_hub/qr_codes/",
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return (
            f"{self.member.member_code} | "
            f"{self.member.first_name} {self.member.last_name}"
        )


    class Meta:
        verbose_name = "Member Hub"
        verbose_name_plural = "Member Hubs"
        ordering = ["member__member_code"]    