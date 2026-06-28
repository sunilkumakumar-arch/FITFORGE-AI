from django.db import models

from accounts.models import Member
from trainers.models import Trainer


class NutritionPlan(models.Model):

    GOAL_CHOICES = [
        ("Weight Loss", "Weight Loss"),
        ("Fat Loss", "Fat Loss"),
        ("Muscle Gain", "Muscle Gain"),
        ("Strength", "Strength"),
        ("General Fitness", "General Fitness"),
    ]

    name = models.CharField(max_length=150)

    goal = models.CharField(
        max_length=50,
        choices=GOAL_CHOICES
    )

    calories = models.PositiveIntegerField()

    protein = models.PositiveIntegerField()

    carbs = models.PositiveIntegerField()

    fats = models.PositiveIntegerField()

    notes = models.TextField(blank=True)

    created_by = models.ForeignKey(
        Trainer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name


class Meal(models.Model):

    nutrition_plan = models.ForeignKey(
        NutritionPlan,
        on_delete=models.CASCADE,
        related_name="meals"
    )

    meal_name = models.CharField(
        max_length=100
    )

    meal_time = models.CharField(
        max_length=50
    )

    foods = models.TextField()

    calories = models.PositiveIntegerField()

    def __str__(self):
        return self.meal_name


class MemberNutritionAssignment(models.Model):

    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name="nutrition_assignments"
    )

    nutrition_plan = models.ForeignKey(
        NutritionPlan,
        on_delete=models.CASCADE,
        related_name="assigned_members"
    )

    assigned_by = models.ForeignKey(
        Trainer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    assigned_date = models.DateField(
        auto_now_add=True
    )

    active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return f"{self.member} - {self.nutrition_plan}"