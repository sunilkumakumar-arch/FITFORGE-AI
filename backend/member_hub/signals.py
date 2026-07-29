from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import Member

from .services import MemberHubService


@receiver(post_save, sender=Member)
def create_member_hub(sender, instance, created, **kwargs):
    """
    Automatically create a MemberHub whenever a new Member is created.
    """

    if not created:
        return

    MemberHubService.create_for_member(instance)