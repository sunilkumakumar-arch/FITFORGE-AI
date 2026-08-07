from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=200)
    owner_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    def __str__(self):
        return self.name


class Branch(models.Model):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="branches"
    )

    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    address = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        ordering = ["organization", "name"]

        unique_together = (
            "organization",
            "name",
        )

        verbose_name = "Branch"

        verbose_name_plural = "Branches"

    def __str__(self):
         return f"{self.organization.name} - {self.name}"



    

class Department(models.Model):

    name = models.CharField(max_length=100, unique=True)

    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name    
    
class Designation(models.Model):

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="designations",
    )

    name = models.CharField(
        max_length=100,
    )

    description = models.TextField(
        blank=True,
    )

    hierarchy_level = models.PositiveIntegerField(
        default=1,
        help_text="Lower number indicates higher designation level.",
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
        ordering = ["department", "hierarchy_level", "name"]
        unique_together = ("department", "name")

    def __str__(self):
        return f"{self.department.name} - {self.name}"    


class Shift(models.Model):
    SHIFT_TYPE_CHOICES = [
        ("GENERAL", "General"),
        ("MORNING", "Morning"),
        ("EVENING", "Evening"),
        ("NIGHT", "Night"),
        ("FLEXIBLE", "Flexible"),
        ("SPLIT", "Split"),
    ]

    name = models.CharField(
        max_length=100,
        unique=True,
    )

    code = models.CharField(
        max_length=20,
        unique=True,
    )

    shift_type = models.CharField(
        max_length=20,
        choices=SHIFT_TYPE_CHOICES,
        default="GENERAL",
    )

    start_time = models.TimeField()

    end_time = models.TimeField()

    grace_period_minutes = models.PositiveIntegerField(
        default=15,
    )

    break_duration_minutes = models.PositiveIntegerField(
        default=30,
    )

    minimum_working_hours = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=8.00,
    )

    weekly_working_days = models.PositiveSmallIntegerField(
        default=6,
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
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.code})"