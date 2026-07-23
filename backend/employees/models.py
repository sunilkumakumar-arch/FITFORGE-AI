from django.db import models
from django.contrib.auth.models import User

from core.models import (
    Organization,
    Branch,
    Department,
    
)

from roles.models import Role


class Employee(models.Model):

    STATUS_CHOICES = [
        ("ACTIVE", "Active"),
        ("ON_LEAVE", "On Leave"),
        ("SUSPENDED", "Suspended"),
        ("TERMINATED", "Terminated"),
    ]

    EMPLOYMENT_TYPE_CHOICES = [
        ("FULL_TIME", "Full Time"),
        ("PART_TIME", "Part Time"),
        ("FREELANCE", "Freelance"),
        ("CONTRACT", "Contract"),
        ("CONSULTANT", "Consultant"),
        ("INTERN", "Intern"),
    ]

    EMPLOYEE_CLASSIFICATION_CHOICES = [
        ("TRAINER", "Trainer"),
        ("SALES_EXECUTIVE", "Sales Executive"),
        ("CENTER_MANAGER", "Center Manager"),
        ("HOUSEKEEPING", "Housekeeping"),
        ("NUTRITIONIST", "Nutritionist"),
        ("PHYSIOTHERAPIST", "Physiotherapist"),
        ("YOGA_INSTRUCTOR", "Yoga Instructor"),
        ("ZUMBA_INSTRUCTOR", "Zumba Instructor"),
        ("OPERATIONS_MANAGER", "Operations Manager"),
        ("HR", "Human Resources"),
        ("ADMIN", "Administrator"),
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

    designation = models.ForeignKey(
        "core.Designation",
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

    confirmation_date = models.DateField(
        null=True,
        blank=True,
    )

    relieving_date = models.DateField(
        null=True,
        blank=True,
    )

    employment_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="ACTIVE",
    )

    employment_type = models.CharField(
        max_length=20,
        choices=EMPLOYMENT_TYPE_CHOICES,
        default="FULL_TIME",
    ) 

    employee_classification = models.CharField(
        max_length=30,
        choices=EMPLOYEE_CLASSIFICATION_CHOICES,
        default="TRAINER",
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

    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    aadhaar_document = models.FileField(
        upload_to="employees/documents/aadhaar/",
        blank=True,
        null=True,
    )

    pan_document = models.FileField(
        upload_to="employees/documents/pan/",
        blank=True,
        null=True,
    )

    resume = models.FileField(
        upload_to="employees/documents/resume/",
        blank=True,
        null=True,
    )

    appointment_letter = models.FileField(
        upload_to="employees/documents/appointment_letters/",
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["employee_code"]

    

    def __str__(self):
        return f"{self.employee_code} - {self.first_name} {self.last_name}"