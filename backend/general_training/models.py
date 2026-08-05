from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from accounts.models import Member
from memberships.models import MemberMembership
from trainers.models import Trainer


class GeneralTrainerAssignment(models.Model):
    """
    Stores General Training (GT) trainer assignments.
    Every member can have only one ACTIVE GT assignment at a time.
    Historical assignments are preserved.
    """

    class AssignmentStatus(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        TRANSFERRED = "TRANSFERRED", "Transferred"
        COMPLETED = "COMPLETED", "Completed"

    class AssignmentMode(models.TextChoices):
        AUTO = "AUTO", "Auto"
        MANUAL = "MANUAL", "Manual"

    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name="general_trainer_assignments",
    )

    membership = models.ForeignKey(
        MemberMembership,
        on_delete=models.CASCADE,
        related_name="general_trainer_assignments",
    )

    trainer = models.ForeignKey(
        Trainer,
        on_delete=models.PROTECT,
        related_name="general_members",
    )

    assignment_status = models.CharField(
        max_length=20,
        choices=AssignmentStatus.choices,
        default=AssignmentStatus.ACTIVE,
    )

    assignment_mode = models.CharField(
        max_length=10,
        choices=AssignmentMode.choices,
        default=AssignmentMode.AUTO,
    )

    start_date = models.DateField()

    end_date = models.DateField(
        null=True,
        blank=True,
    )

    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="gt_assignments_created",
    )

    notes = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "General Trainer Assignment"
        verbose_name_plural = "General Trainer Assignments"

    def clean(self):
        if (
            self.assignment_status == self.AssignmentStatus.ACTIVE
            and GeneralTrainerAssignment.objects.exclude(pk=self.pk)
            .filter(
                member=self.member,
                assignment_status=self.AssignmentStatus.ACTIVE,
            )
            .exists()
        ):
            raise ValidationError(
                "Member already has an active General Trainer assignment."
            )

    def __str__(self):
        return f"{self.member} → {self.trainer}"



class GeneralTrainerChangeHistory(models.Model):

    class ChangeReason(models.TextChoices):
        TIMING = "TIMING", "Timing"
        AVAILABILITY = "AVAILABILITY", "Trainer Availability"
        COMMUNICATION = "COMMUNICATION", "Communication"
        BEHAVIOUR = "BEHAVIOUR", "Behaviour"
        KNOWLEDGE = "KNOWLEDGE", "Knowledge"
        SPECIALIZATION = "SPECIALIZATION", "Need Different Specialization"
        LOCATION = "LOCATION", "Location"
        MEMBER_REQUEST = "MEMBER_REQUEST", "Member Requested"
        MANAGEMENT = "MANAGEMENT", "Management Decision"
        OTHER = "OTHER", "Other"

    assignment = models.ForeignKey(
        GeneralTrainerAssignment,
        on_delete=models.CASCADE,
        related_name="change_history",
    )

    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
    )

    old_trainer = models.ForeignKey(
        Trainer,
        on_delete=models.PROTECT,
        related_name="gt_old_assignments",
    )

    new_trainer = models.ForeignKey(
        Trainer,
        on_delete=models.PROTECT,
        related_name="gt_new_assignments",
    )

    reason = models.CharField(
        max_length=30,
        choices=ChangeReason.choices,
    )

    rating = models.PositiveSmallIntegerField()

    comments = models.TextField(
        blank=True,
    )

    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
    )

    changed_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-changed_at"]
        verbose_name = "General Trainer Change History"
        verbose_name_plural = "General Trainer Change History"

    def clean(self):
        if self.rating < 1 or self.rating > 5:
            raise ValidationError(
                {"rating": "Rating must be between 1 and 5."}
            )

    def __str__(self):
        return (
            f"{self.member} : "
            f"{self.old_trainer} → {self.new_trainer}"
        )
    