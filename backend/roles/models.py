from django.db import models
from django.contrib.auth.models import User


class Role(models.Model):

    ROLE_CHOICES = [
        ("SUPER_ADMIN", "Super Admin"),
        ("MANAGER", "Manager"),
        ("TRAINER", "Trainer"),
        ("RECEPTIONIST", "Receptionist"),
        ("MEMBER", "Member"),
    ]

    name = models.CharField(
        max_length=30,
        choices=ROLE_CHOICES,
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name


class UserRole(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="role_assignment"
    )

    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name="users"
    )

    assigned_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.role.name}"