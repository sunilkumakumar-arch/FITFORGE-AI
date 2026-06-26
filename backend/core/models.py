from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=200)
    owner_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)

    created_at = models.DateTimeField(auto_now_add=True)

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

class Meta:
    verbose_name = "Branch"
    verbose_name_plural = "Branches"

    def __str__(self):
        return f"{self.organization.name} - {self.name}"


class Role(models.Model):
    ROLE_CHOICES = [
        ("SUPER_ADMIN", "Super Admin"),
        ("ORG_OWNER", "Organization Owner"),
        ("BRANCH_MANAGER", "Branch Manager"),
        ("FITNESS_CONSULTANT", "Fitness Consultant"),
        ("RECEPTIONIST", "Receptionist"),
        ("SALES_EXECUTIVE", "Sales Executive"),
        ("TRAINER", "Trainer"),
        ("FREELANCE_TRAINER", "Freelance Trainer"),
        ("MEMBER", "Gym Member"),
        ("ONLINE_MEMBER", "Online Member"),
        ("ACCOUNTANT", "Accountant"),
        ("HR", "HR"),
    ]

    name = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES,
        unique=True
    )

    def __str__(self):
        return self.get_name_display()