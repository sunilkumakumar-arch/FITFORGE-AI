from django.db import models
from employees.models import Employee


class Trainer(models.Model):

    EMPLOYMENT_STATUS = [
        ("Active", "Active"),
        ("Inactive", "Inactive"),
        ("On Leave", "On Leave"),
        ("Terminated", "Terminated"),
    ]

    SHIFT_CHOICES = [
        ("SHIFT_1", "6AM-10:30AM & 5PM-9:30PM"),
        ("SHIFT_2", "6AM-10:30AM & 5:30PM-10PM"),
        ("SHIFT_3", "6AM-3PM"),
        ("SHIFT_4", "1PM-10PM"),
        ("SHIFT_5", "5:30AM-2:30PM"),
        ("SHIFT_6", "12PM-9PM"),
    ]

    TRAINER_STATUS = [
        ("On Duty", "On Duty"),
        ("On Break", "On Break"),
        ("Off Duty", "Off Duty"),
        ("Leave", "Leave"),
    ]

    TRAINER_LEVELS = [
        ("LEVEL_1", "Level 1"),
        ("LEVEL_2", "Level 2"),
        ("LEVEL_3", "Level 3"),
        ("LEVEL_4", "Level 4"),
    ]

    trainer_level = models.CharField(
        
        max_length=10,
        choices=TRAINER_LEVELS,
        default="LEVEL_1"
    )

    trainer_capacity = models.PositiveIntegerField(
        default=40
    )

    

    trainer_code = models.CharField(
        max_length=20,
        unique=True,
        blank=True
    )

    first_name = models.CharField(max_length=100)


    last_name = models.CharField(max_length=100)

    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )

    gender = models.CharField(
        max_length=10,
        choices=[
            ("Male", "Male"),
            ("Female", "Female"),
            ("Other", "Other"),
        ],
        blank=True,
    )

    phone = models.CharField(
        max_length=15
    )

    email = models.EmailField(
        blank=True
    )

    alternate_phone = models.CharField(
        max_length=15,
        blank=True,
    )

    aadhaar_number = models.CharField(
        max_length=12,
        blank=True,
    )

    pan_number = models.CharField(
        max_length=10,
        blank=True,
    )

    specialization = models.CharField(
        max_length=200,
        
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
    aadhaar_document = models.FileField(
        upload_to="trainers/documents/aadhaar/",
        blank=True,
        null=True,
    )

    pan_document = models.FileField(
        upload_to="trainers/documents/pan/",
        blank=True,
        null=True,
    )

    resume = models.FileField(
        upload_to="trainers/documents/resume/",
        blank=True,
        null=True,
    )

    appointment_letter = models.FileField(
        upload_to="trainers/documents/appointment_letters/",
        blank=True,
        null=True,
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

    shift_type = models.CharField(
        max_length=20,
        choices=SHIFT_CHOICES,
        default="SHIFT_3"
    )

    trainer_status = models.CharField(
        max_length=20,
        choices=TRAINER_STATUS,
        default="Off Duty"
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

    address = models.TextField(
        blank=True,
    )

    city = models.CharField(
        max_length=100,
        blank=True,
    )

    state = models.CharField(
        max_length=100,
        blank=True,
    )

    pincode = models.CharField(
        max_length=10,
        blank=True,
    )

    blood_group = models.CharField(
        max_length=5,
        blank=True,
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

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()    

    def __str__(self):
        return (
            f"{self.trainer_code} - "
            f"{self.first_name} {self.last_name}"
        )


class TrainerCertification(models.Model):

    trainer = models.ForeignKey(
        Trainer,
        on_delete=models.CASCADE,
        related_name="trainer_certifications",
    )

    certification = models.ForeignKey(
        "certifications.Certification",
        on_delete=models.CASCADE,
    )


    certificate_number = models.CharField(
        max_length=100,
        blank=True,
    )

    issue_date = models.DateField(
        null=True,
        blank=True,
    )

    expiry_date = models.DateField(
        null=True,
        blank=True,
    )

    certificate_file = models.FileField(
        upload_to="trainer_certificates/",
        null=True,
        blank=True,
    )

    verification_status = models.CharField(
        max_length=20,
        choices=[
            ("Pending", "Pending"),
            ("Verified", "Verified"),
            ("Rejected", "Rejected"),
            ("Expired", "Expired"),
        ],
        default="Pending",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        unique_together = (
            "trainer",
            "certification",
        )

    def __str__(self):
        return f"{self.trainer} - {self.certification}"

class TrainerWeeklyOff(models.Model):

    DAY_CHOICES = [
        ("Monday", "Monday"),
        ("Tuesday", "Tuesday"),
        ("Wednesday", "Wednesday"),
        ("Thursday", "Thursday"),
        ("Friday", "Friday"),
        ("Saturday", "Saturday"),
        ("Sunday", "Sunday"),
    ]

    trainer = models.ForeignKey(
        Trainer,
        on_delete=models.CASCADE,
        related_name="weekly_offs"
    )

    week_start_date = models.DateField()

    off_day = models.CharField(
        max_length=20,
        choices=DAY_CHOICES
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.trainer.first_name} - "
            f"{self.off_day}"
        )   





class TrainerProfile(models.Model):

    TRAINER_STATUS = [
        ("On Duty", "On Duty"),
        ("On Break", "On Break"),
        ("Off Duty", "Off Duty"),
        ("Leave", "Leave"),
    ]

    SHIFT_CHOICES = [
        ("SHIFT_1", "6AM-10:30AM & 5PM-9:30PM"),
        ("SHIFT_2", "6AM-10:30AM & 5:30PM-10PM"),
        ("SHIFT_3", "6AM-3PM"),
        ("SHIFT_4", "1PM-10PM"),
        ("SHIFT_5", "5:30AM-2:30PM"),
        ("SHIFT_6", "12PM-9PM"),
    ]

    TRAINER_LEVELS = [
        ("LEVEL_1", "Level 1"),
        ("LEVEL_2", "Level 2"),
        ("LEVEL_3", "Level 3"),
        ("LEVEL_4", "Level 4"),
    ]

    employee = models.OneToOneField(
        Employee,
        on_delete=models.CASCADE,
        related_name="trainer_profile",
    )

    trainer_level = models.CharField(
        max_length=10,
        choices=TRAINER_LEVELS,
        default="LEVEL_1",
    )

    specialization = models.CharField(
        max_length=200,
        blank=True,
    )

    experience_years = models.PositiveIntegerField(
        default=0,
    )

    trainer_capacity = models.PositiveIntegerField(
        default=40,
    )

    trainer_status = models.CharField(
        max_length=20,
        choices=TRAINER_STATUS,
        default="Off Duty",
    )

    shift_type = models.CharField(
        max_length=20,
        choices=SHIFT_CHOICES,
        default="SHIFT_3",
    )

    commission_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
    )

    active_clients = models.PositiveIntegerField(
        default=0,
    )

    total_clients_trained = models.PositiveIntegerField(
        default=0,
    )

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0,
    )

    available_for_pt = models.BooleanField(
        default=True,
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
        ordering = ["employee__employee_code"]

    def __str__(self):
        return (
            f"{self.employee.employee_code} - "
            f"{self.employee.first_name} "
            f"{self.employee.last_name}"
        )     
    

    