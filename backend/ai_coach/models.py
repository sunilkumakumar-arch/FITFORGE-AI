from django.db import models

from accounts.models import Member


class AICoachRequest(models.Model):

    REQUEST_TYPES = [
        ("WORKOUT", "Workout"),
        ("NUTRITION", "Nutrition"),
        ("POSTURE", "Posture"),
    ]

    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name="ai_requests",
    )

    request_type = models.CharField(
        max_length=20,
        choices=REQUEST_TYPES,
    )

    input_data = models.JSONField()

    ai_response = models.JSONField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.member} - {self.request_type}"
    
class PostureAssessment(models.Model):

    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name="posture_assessments",
    )

    front_image = models.ImageField(
        upload_to="posture/front/"
    )

    back_image = models.ImageField(
        upload_to="posture/back/"
    )

    left_image = models.ImageField(
        upload_to="posture/left/"
    )

    right_image = models.ImageField(
        upload_to="posture/right/"
    )

    posture_score = models.IntegerField(
        default=0
    )

    findings = models.JSONField(
        default=dict
    )

    corrective_plan = models.JSONField(
        default=dict
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Posture Assessment - {self.member}"    