from django.db import models
from django.conf import settings


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    phone_verified = models.BooleanField(default=False)

    must_change_password = models.BooleanField(default=True)

    account_locked = models.BooleanField(default=False)

    failed_login_attempts = models.PositiveIntegerField(default=0)

    last_password_change = models.DateTimeField(
        null=True,
        blank=True,
    )

    profile_photo = models.ImageField(
        upload_to="users/profile_photos/",
        null=True,
        blank=True,
    )

    timezone = models.CharField(
        max_length=100,
        default="Asia/Kolkata",
    )

    language = models.CharField(
        max_length=20,
        default="en",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return self.user.username