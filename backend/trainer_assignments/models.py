from django.db import models
from django.core.exceptions import ValidationError

from trainers.models import Trainer
from accounts.models import Member


class TrainerAssignment(models.Model):

    trainer = models.ForeignKey(
        Trainer,
        on_delete=models.CASCADE,
        related_name="assignments",
        null=True,
        blank=True,
    )

    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name="trainer_assignments"
    )

    start_date = models.DateField()

    end_date = models.DateField(
        null=True,
        blank=True
    )

    monthly_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    sessions_per_week = models.PositiveIntegerField(
        default=3
    )

    assignment_type = models.CharField(
        max_length=20,
        choices=[
            ("MEMBERSHIP", "Membership"),
            ("PT", "Personal Training"),
        ],
        default="MEMBERSHIP"
    )

    package_type = models.CharField(
        max_length=20,
        choices=[
            ("3_DAYS", "3 Days Per Week"),
            ("6_DAYS", "6 Days Per Week"),
        ],
        default="3_DAYS"
    )

    goal_type = models.CharField(
        max_length=30,
        choices=[
            ("WEIGHT_LOSS", "Weight Loss"),
            ("FAT_LOSS", "Fat Loss"),
            ("MUSCLE_GAIN", "Muscle Gain"),
            ("STRENGTH", "Strength"),
            ("GENERAL_FITNESS", "General Fitness"),
        ],
        default="GENERAL_FITNESS"
    )

    slot_time = models.TimeField(
        null=True,
        blank=True
    )

    slot_capacity = models.PositiveIntegerField(
        default=2
    )

    slot_position = models.PositiveIntegerField(
        default=1
    )

    day_pattern = models.CharField(
        max_length=20,
        choices=[
            ("ALL_DAYS", "All Days"),
            ("MWF", "Monday Wednesday Friday"),
            ("TTS", "Tuesday Thursday Saturday"),
            
        ],
        default="ALL_DAYS"
    )

    auto_assigned = models.BooleanField(
        default=False
    )

    weekly_off_considered = models.BooleanField(
        default=True
    )

    is_active = models.BooleanField(
        default=True
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

    class Meta:
        ordering = ["-created_at"]

        indexes = [
            models.Index(
                fields=[
                    "trainer",
                    "slot_time",
                    "day_pattern",
                ]
            ),
        ]

    def clean(self):

        # ----------------------------------
        # MEMBERSHIP ASSIGNMENT
        # ----------------------------------

        if self.assignment_type == "MEMBERSHIP":
            return

        # ----------------------------------
        # PT ASSIGNMENT VALIDATION
        # ----------------------------------

        if not self.trainer:
            raise ValidationError(
                "Trainer is required for PT assignments."
            )

        if not self.slot_time:
            raise ValidationError(
                "Slot time is required for PT assignments."
            )

        existing_assignments = (
            TrainerAssignment.objects
            .filter(
                trainer=self.trainer,
                slot_time=self.slot_time,
                is_active=True,
                assignment_type="PT",
            )
            .exclude(id=self.id)
        )

        # ----------------------------------
        # SLOT CAPACITY
        # ----------------------------------

        if existing_assignments.count() >= 2:
            raise ValidationError(
                "Selected trainer slot is full."
            )

        # ----------------------------------
        # GOAL COMPATIBILITY
        # ----------------------------------

        existing_goals = set(
            existing_assignments.values_list(
                "goal_type",
                flat=True
            )
        )

        existing_goals.discard(None)

        if existing_goals:

            slot_goal = list(existing_goals)[0]

            if slot_goal != self.goal_type:
                raise ValidationError(
                    f"Slot already reserved for {slot_goal}."
                )

        # ----------------------------------
        # DAY PATTERN VALIDATION
        # ----------------------------------

        existing_patterns = list(
            existing_assignments.values_list(
                "day_pattern",
                flat=True
            )
        )

        if (
            self.day_pattern == "ALL"
            and existing_patterns
        ):
            raise ValidationError(
                "Cannot assign ALL pattern. Slot already occupied."
            )

        if "ALL" in existing_patterns:
            raise ValidationError(
                "Slot already occupied by ALL pattern client."
            )

        if (
            self.day_pattern == "MWF"
            and existing_patterns.count("MWF") >= 1
        ):
            raise ValidationError(
                "MWF slot already occupied."
            )

        if (
            self.day_pattern == "TTS"
            and existing_patterns.count("TTS") >= 1
        ):
            raise ValidationError(
                "TTS slot already occupied."
            )

    def save(self, *args, **kwargs):

        self.full_clean()

        if (
            self.assignment_type == "PT"
            and not self.slot_position
        ):

            existing = (
                TrainerAssignment.objects
                .filter(
                    trainer=self.trainer,
                    slot_time=self.slot_time,
                    is_active=True
                )
                .count()
            )

            self.slot_position = existing + 1

        super().save(*args, **kwargs)

    def __str__(self):

        if self.trainer:
            return f"{self.member} → {self.trainer}"

        return f"{self.member} → Membership Assignment"