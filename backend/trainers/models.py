from django.db import models


class Trainer(models.Model):

    EMPLOYMENT_STATUS = [
        ("Active", "Active"),
        ("Inactive", "Inactive"),
        ("On Leave", "On Leave"),
        ("Terminated", "Terminated"),
    ]

    trainer_code = models.CharField(
        max_length=20,
        unique=True,
        blank=True
    )

    first_name = models.CharField(max_length=100)

    last_name = models.CharField(max_length=100)

    phone = models.CharField(max_length=15)

    email = models.EmailField(blank=True)

    specialization = models.CharField(
        max_length=100,
        blank=True
    )

    certifications = models.TextField(
        blank=True
    )

    experience_years = models.PositiveIntegerField(
        default=0
    )

    photo = models.ImageField(
        upload_to="trainers/photos/",
        blank=True,
        null=True
    )

    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    commission_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )
    active_clients = models.PositiveIntegerField(
    default=0
    )

    total_clients_trained = models.PositiveIntegerField(
     default=0
    )

    rating = models.DecimalField(
    max_digits=3,
    decimal_places=2,
    default=0
    )

    available_for_pt = models.BooleanField(
    default=True
    )


    emergency_contact_name = models.CharField(
        max_length=100,
        blank=True
    )

    emergency_contact_phone = models.CharField(
        max_length=15,
        blank=True
    )

    employment_status = models.CharField(
        max_length=20,
        choices=EMPLOYMENT_STATUS,
        default="Active"
    )

    joining_date = models.DateField(
        auto_now_add=True
    )

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
    auto_now_add=True,
    null=True,
    blank=True
)

    updated_at = models.DateTimeField(
    auto_now=True,
    null=True,
    blank=True
)
    class Meta:
        ordering = ["trainer_code"]

    def save(self, *args, **kwargs):

        if not self.trainer_code:

            last_trainer = (
                Trainer.objects
                .exclude(trainer_code="")
                .order_by("-trainer_code")
                .first()
            )

            if last_trainer:
                last_number = int(
                    last_trainer.trainer_code.replace("TRN", "")
                )
                self.trainer_code = f"TRN{last_number + 1:06d}"
            else:
                self.trainer_code = "TRN000001"

        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.trainer_code} - "
            f"{self.first_name} {self.last_name}"
        )