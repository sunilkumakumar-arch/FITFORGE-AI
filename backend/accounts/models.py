from django.db import models

class Member(models.Model):

    first_name = models.CharField(
        max_length=100
    )

    last_name = models.CharField(
        max_length=100
    )

    phone = models.CharField(
        max_length=15,
        unique=True
    )

    email = models.EmailField(
        blank=True,
        unique=True
    )

    gender = models.CharField(
        max_length=10
    )

    date_of_birth = models.DateField()

    joining_date = models.DateField(
        auto_now_add=True
    )

    # =====================================
    # TRAINER ASSIGNMENT PROFILE
    # =====================================

    preferred_slot = models.CharField(
        max_length=20,
        blank=True,
        default=""
    )

    experience_level = models.CharField(
        max_length=20,
        blank=True,
        default=""
    )

    trainer_preference = models.CharField(
        max_length=20,
        blank=True,
        default=""
    )

    def __str__(self):
        return (
            f"{self.first_name} "
            f"{self.last_name}"
        )
    

class MemberProfile(models.Model):
    member = models.OneToOneField(
        Member,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    member_code = models.CharField(max_length=30, unique=True)

    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, default="India")
    pin_code = models.CharField(max_length=10, blank=True)

    occupation = models.CharField(max_length=100, blank=True)

    profile_photo = models.ImageField(
        upload_to="members/profile_photos/",
        blank=True,
        null=True
    )

    qr_code = models.ImageField(
        upload_to="members/qr_codes/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.member} Profile"
    
class EmergencyContact(models.Model):
    member = models.OneToOneField(
        Member,
        on_delete=models.CASCADE,
        related_name="emergency_contact"
    )

    contact_name = models.CharField(max_length=100)

    relationship = models.CharField(max_length=50)

    phone = models.CharField(max_length=15)

    alternate_phone = models.CharField(
        max_length=15,
        blank=True
    )

    address = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.member} - {self.contact_name}"
    
class MedicalProfile(models.Model):
    member = models.OneToOneField(
        Member,
        on_delete=models.CASCADE,
        related_name="medical_profile"
    )

    blood_group = models.CharField(max_length=5, blank=True)

    medical_conditions = models.TextField(blank=True)

    allergies = models.TextField(blank=True)

    medications = models.TextField(blank=True)

    previous_injuries = models.TextField(blank=True)

    surgeries = models.TextField(blank=True)

    doctor_name = models.CharField(
        max_length=100,
        blank=True
    )

    doctor_phone = models.CharField(
        max_length=15,
        blank=True
    )

    emergency_notes = models.TextField(blank=True)

    parq_completed = models.BooleanField(default=False)

    medical_clearance = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.member} Medical Profile"    
    

class FitnessGoal(models.Model):
    GOAL_CHOICES = [
        ("weight_loss", "Weight Loss"),
        ("muscle_gain", "Muscle Gain"),
        ("fat_loss", "Fat Loss"),
        ("general_fitness", "General Fitness"),
        ("strength", "Strength"),
        ("sports_performance", "Sports Performance"),
        ("rehabilitation", "Rehabilitation"),
        ("competition", "Competition"),
    ]

    member = models.OneToOneField(
        Member,
        on_delete=models.CASCADE,
        related_name="fitness_goal"
    )

    primary_goal = models.CharField(
        max_length=50,
        choices=GOAL_CHOICES
    )

    target_weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )

    target_body_fat = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )

    target_date = models.DateField(
        null=True,
        blank=True
    )

    trainer_notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.member} - {self.primary_goal}"    
    
class BodyAssessment(models.Model):
    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name="body_assessments"
    )

    assessment_date = models.DateField()

    height = models.DecimalField(max_digits=5, decimal_places=2)

    weight = models.DecimalField(max_digits=5, decimal_places=2)

    bmi = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )

    body_fat_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )

    skeletal_muscle = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )

    chest = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    waist = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    hips = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    left_arm = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    right_arm = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    left_thigh = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    right_thigh = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    left_calf = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    right_calf = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.member} - {self.assessment_date}"    