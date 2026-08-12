from django.db import models

from core.models import Branch


class GymFacility(models.Model):

    name = models.CharField(
        max_length=200,
    )

    code = models.CharField(
        max_length=30,
    )

    branch = models.ForeignKey(
        Branch,
        on_delete=models.PROTECT,
        related_name="gym_facilities",
    )

    description = models.TextField(
        blank=True,
    )

    capacity = models.PositiveIntegerField(
        default=0,
    )

    area_sqft = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
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
        ordering = [
            "branch",
            "name",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "branch",
                    "name",
                ],
                name="unique_facility_name_per_branch",
            ),
            models.UniqueConstraint(
                fields=[
                    "branch",
                    "code",
                ],
                name="unique_facility_code_per_branch",
            ),
        ]

        indexes = [
            models.Index(
                fields=[
                    "branch",
                    "is_active",
                ]
            ),
            models.Index(
                fields=[
                    "code",
                ]
            ),
        ]

    def __str__(self):
        return f"{self.branch} - {self.name}"


class GymZone(models.Model):

    ZONE_TYPE_CHOICES = [
        ("CARDIO", "Cardio"),
        ("STRENGTH", "Strength"),
        ("FREE_WEIGHTS", "Free Weights"),
        ("FUNCTIONAL", "Functional"),
        ("CROSSFIT", "CrossFit"),
        ("GROUP_CLASS", "Group Class"),
        ("PERSONAL_TRAINING", "Personal Training"),
        ("RECOVERY", "Recovery"),
        ("OTHER", "Other"),
    ]

    facility = models.ForeignKey(
        GymFacility,
        on_delete=models.PROTECT,
        related_name="zones",
    )

    name = models.CharField(
        max_length=150,
    )

    code = models.CharField(
        max_length=30,
    )

    zone_type = models.CharField(
        max_length=30,
        choices=ZONE_TYPE_CHOICES,
        default="OTHER",
    )

    capacity = models.PositiveIntegerField(
        default=0,
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
        ordering = [
            "facility",
            "name",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "facility",
                    "name",
                ],
                name="unique_zone_name_per_facility",
            ),
            models.UniqueConstraint(
                fields=[
                    "facility",
                    "code",
                ],
                name="unique_zone_code_per_facility",
            ),
        ]

        indexes = [
            models.Index(
                fields=[
                    "facility",
                    "is_active",
                ]
            ),
            models.Index(
                fields=[
                    "zone_type",
                ]
            ),
        ]

    def __str__(self):
        return f"{self.facility.name} - {self.name}"


class Equipment(models.Model):

    EQUIPMENT_STATUS_CHOICES = [
        ("ACTIVE", "Active"),
        ("MAINTENANCE", "Under Maintenance"),
        ("OUT_OF_ORDER", "Out of Order"),
        ("RETIRED", "Retired"),
    ]

    branch = models.ForeignKey(
        Branch,
        on_delete=models.PROTECT,
        related_name="gym_equipment",
    )

    zone = models.ForeignKey(
        GymZone,
        on_delete=models.PROTECT,
        related_name="equipment",
        null=True,
        blank=True,
    )

    name = models.CharField(
        max_length=200,
    )

    code = models.CharField(
        max_length=50,
    )

    category = models.CharField(
        max_length=100,
    )

    manufacturer = models.CharField(
        max_length=150,
        blank=True,
    )

    model_number = models.CharField(
        max_length=100,
        blank=True,
    )

    serial_number = models.CharField(
        max_length=150,
        blank=True,
    )

    purchase_date = models.DateField(
        null=True,
        blank=True,
    )

    warranty_expiry = models.DateField(
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=30,
        choices=EQUIPMENT_STATUS_CHOICES,
        default="ACTIVE",
    )

    purchase_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    notes = models.TextField(
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
        ordering = [
            "branch",
            "name",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "branch",
                    "code",
                ],
                name="unique_equipment_code_per_branch",
            ),
        ]

        indexes = [
            models.Index(
                fields=[
                    "branch",
                    "status",
                ]
            ),
            models.Index(
                fields=[
                    "category",
                ]
            ),
            models.Index(
                fields=[
                    "serial_number",
                ]
            ),
        ]

    def __str__(self):
        return f"{self.code} - {self.name}"


class EquipmentMaintenance(models.Model):

    MAINTENANCE_STATUS_CHOICES = [
        ("SCHEDULED", "Scheduled"),
        ("IN_PROGRESS", "In Progress"),
        ("COMPLETED", "Completed"),
        ("CANCELLED", "Cancelled"),
    ]

    MAINTENANCE_TYPE_CHOICES = [
        ("PREVENTIVE", "Preventive"),
        ("CORRECTIVE", "Corrective"),
        ("INSPECTION", "Inspection"),
        ("EMERGENCY", "Emergency"),
    ]

    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.PROTECT,
        related_name="maintenance_records",
    )

    maintenance_type = models.CharField(
        max_length=30,
        choices=MAINTENANCE_TYPE_CHOICES,
        default="PREVENTIVE",
    )

    scheduled_date = models.DateField()

    completed_date = models.DateField(
        null=True,
        blank=True,
    )

    vendor = models.CharField(
        max_length=200,
        blank=True,
    )

    cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    status = models.CharField(
        max_length=30,
        choices=MAINTENANCE_STATUS_CHOICES,
        default="SCHEDULED",
    )

    notes = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = [
            "-scheduled_date",
            "-id",
        ]

        indexes = [
            models.Index(
                fields=[
                    "equipment",
                    "status",
                ]
            ),
            models.Index(
                fields=[
                    "scheduled_date",
                ]
            ),
        ]

    def __str__(self):
        return (
            f"{self.equipment.name} - "
            f"{self.scheduled_date}"
        )