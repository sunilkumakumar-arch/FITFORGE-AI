from django.db import models
from django.contrib.auth.models import User


class Role(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True,
    )

    description = models.TextField(
        blank=True,
    )

    is_system_role = models.BooleanField(
        default=False,
    )

    is_active = models.BooleanField(
        default=True,
    )

    permissions = models.ManyToManyField(
        "Permission",
        blank=True,
        related_name="roles",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
    

class Permission(models.Model):

    module = models.CharField(
        max_length=50,
    )

    code = models.CharField(
        max_length=100,
        unique=True,
    )

    name = models.CharField(
        max_length=150,
    )

    description = models.TextField(
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["module", "name"]

    def __str__(self):
        return self.code    
    
    


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