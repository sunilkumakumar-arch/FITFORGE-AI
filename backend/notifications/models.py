from django.db import models

from accounts.models import Member


class Notification(models.Model):

    TYPE_CHOICES = [
        ("Membership", "Membership"),
        ("Payment", "Payment"),
        ("Attendance", "Attendance"),
        ("Workout", "Workout"),
        ("Nutrition", "Nutrition"),
        ("General", "General"),
    ]

    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    notification_type = models.CharField(
        max_length=50,
        choices=TYPE_CHOICES
    )

    title = models.CharField(
        max_length=200
    )

    message = models.TextField()

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title