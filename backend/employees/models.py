from django.db import models
from django.contrib.auth.models import User

from core.models import (
    Organization,
    Branch,
    Department,
    Role,
)


class Employee(models.Model):

    STATUS_CHOICES = [
        ("ACTIVE", "Active"),
        ("ON_LEAVE", "On Leave"),
        ("SUSPENDED", "Suspended"),
        ("TERMINATED", "Terminated"),
    ]

    employee_code = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
    )

    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="employee_profile",
    )

    first_name = models.CharField(max_length=100)

    last_name = models.CharField(max_length=100)

    email = models.EmailField(unique=True)

    phone = models.CharField(max_length=15)

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="employees",
    )

    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name="employees",
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="employees",
    )

    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="employees",
    )

    joining_date = models.DateField()

    employment_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="ACTIVE",
    )

    profile_photo = models.ImageField(
        upload_to="employees/profile_photos/",
        blank=True,
        null=True,
    )

    emergency_contact_name = models.CharField(
        max_length=100,
        blank=True,
    )

    emergency_contact_phone = models.CharField(
        max_length=15,
        blank=True,
    )

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["employee_code"]

    def save(self, *args, **kwargs):

        if not self.employee_code:

            last_employee = (
                Employee.objects
                .filter(employee_code__startswith="EMP")
                .order_by("-employee_code")
                .first()
            )

            if last_employee:
                last_number = int(
                    last_employee.employee_code.replace("EMP", "")
                )
                self.employee_code = f"EMP{last_number + 1:06d}"
            else:
                self.employee_code = "EMP000001"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee_code} - {self.first_name} {self.last_name}"