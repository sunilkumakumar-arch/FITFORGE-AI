from django.db import models
from django.core.exceptions import ValidationError
from accounts.models import Member
from trainers.models import Trainer
from core.models import Branch


class Attendance(models.Model):

    STATUS_CHOICES = [
        ("Present", "Present"),
        ("Absent", "Absent"),
        ("Late", "Late"),
    ]

    CHECKIN_METHODS = [
        ("Reception", "Reception"),
        ("QR", "QR Code"),
        ("Manual", "Manual"),
        ("Mobile", "Mobile App"),
    ]

    member = models.ForeignKey(
    Member,
    on_delete=models.CASCADE,
    related_name="attendance_records"
)

    trainer = models.ForeignKey(
        Trainer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE
    )

    attendance_date = models.DateField()

    check_in = models.DateTimeField()

    check_out = models.DateTimeField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Present"
    )

    checkin_method = models.CharField(
        max_length=20,
        choices=CHECKIN_METHODS,
        default="Reception"
    )

    device_id = models.CharField(
        max_length=100,
        blank=True
    )

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-attendance_date", "-check_in"]
        unique_together = ("member", "attendance_date")

    def clean(self):
        if self.check_out and self.check_out < self.check_in:
            raise ValidationError(
                "Check-out cannot be earlier than check-in."
            )

    @property
    def workout_duration(self):
        if self.check_out:
            return self.check_out - self.check_in
        return None

    def __str__(self):
        return f"{self.member} - {self.attendance_date}"