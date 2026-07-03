# leads/models.py

from django.db import models


class Lead(models.Model):

    SOURCE_CHOICES = [
        ("Walk-In", "Walk-In"),
        ("Instagram", "Instagram"),
        ("Facebook", "Facebook"),
        ("Google", "Google"),
        ("Website", "Website"),
        ("Referral", "Referral"),
        ("Other", "Other"),
    ]

    STATUS_CHOICES = [
        ("New", "New"),
        ("Contacted", "Contacted"),
        ("Follow-Up", "Follow-Up"),
        ("Trial Scheduled", "Trial Scheduled"),
        ("Converted", "Converted"),
        ("Lost", "Lost"),
    ]

    first_name = models.CharField(max_length=100)

    last_name = models.CharField(
        max_length=100,
        blank=True
    )

    phone = models.CharField(max_length=15)

    email = models.EmailField(
        blank=True
    )

    gender = models.CharField(
        max_length=20,
        blank=True
    )

    age = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    fitness_goal = models.CharField(
        max_length=255,
        blank=True
    )

    source = models.CharField(
        max_length=50,
        choices=SOURCE_CHOICES,
        default="Walk-In"
    )

    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default="New"
    )

    interested_plan = models.CharField(
        max_length=100,
        blank=True
    )

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return (
            f"{self.first_name} "
            f"{self.last_name}"
        )


class LeadFollowUp(models.Model):

    lead = models.ForeignKey(
        Lead,
        on_delete=models.CASCADE,
        related_name="followups"
    )

    followup_date = models.DateField()

    remarks = models.TextField()

    next_followup_date = models.DateField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.lead} - "
            f"{self.followup_date}"
        )