from django.db import models

from django.utils import timezone

class UserProfile(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)

    age = models.IntegerField()
    gender = models.CharField(max_length=10)

    height = models.FloatField()
    weight = models.FloatField()

    goal = models.CharField(max_length=100)

    membership_start = models.DateField()
    membership_end = models.DateField()

    emergency_contact = models.CharField(max_length=20)

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.full_name

class Trainer(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    experience_years = models.IntegerField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Membership(models.Model):
    member = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE
    )

    plan_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    start_date = models.DateField()
    end_date = models.DateField()

    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.member.full_name} - {self.plan_name}"
    
class Payment(models.Model):
    member = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_date = models.DateField()

    payment_method = models.CharField(
        max_length=50
    )

    transaction_id = models.CharField(
        max_length=100
    )

    status = models.CharField(
        max_length=20,
        default="Paid"
    )

    def __str__(self):
        return f"{self.member.full_name} - {self.amount}"

class Attendance(models.Model):
    member = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE
    )

    check_in = models.DateTimeField(
        auto_now_add=True
    )

    status = models.CharField(
        max_length=20,
        default="Present"
    )

    def __str__(self):
        return f"{self.member.full_name} - {self.check_in.date()}"    

class WorkoutPlan(models.Model):
    member = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE
    )

    trainer = models.ForeignKey(
        Trainer,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=100)

    description = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.member.full_name} - {self.title}"

class DietPlan(models.Model):
    member = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE
    )

    trainer = models.ForeignKey(
        Trainer,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=100)

    breakfast = models.TextField()
    lunch = models.TextField()
    dinner = models.TextField()
    snacks = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.member.full_name} - {self.title}"        