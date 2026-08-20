from django.db import transaction
from rest_framework.exceptions import ValidationError

from nutrition.models import Meal


class NutritionMealService:
    """
    Business logic for managing meals within nutrition plans.
    """

    @staticmethod
    @transaction.atomic
    def create_meal(
        *,
        nutrition_plan,
        meal_name,
        meal_time,
        foods,
        calories,
    ):
        """
        Create a meal under a nutrition plan.
        """

        if not nutrition_plan:
            raise ValidationError(
                {
                    "nutrition_plan": (
                        "Nutrition plan is required."
                    )
                }
            )

        if not meal_name:
            raise ValidationError(
                {
                    "meal_name": (
                        "Meal name is required."
                    )
                }
            )

        if not meal_time:
            raise ValidationError(
                {
                    "meal_time": (
                        "Meal time is required."
                    )
                }
            )

        if not foods:
            raise ValidationError(
                {
                    "foods": (
                        "Foods are required."
                    )
                }
            )

        if calories is None:
            raise ValidationError(
                {
                    "calories": (
                        "Calories are required."
                    )
                }
            )

        if calories < 0:
            raise ValidationError(
                {
                    "calories": (
                        "Calories cannot be negative."
                    )
                }
            )

        return Meal.objects.create(
            nutrition_plan=nutrition_plan,
            meal_name=meal_name,
            meal_time=meal_time,
            foods=foods,
            calories=calories,
        )

    @staticmethod
    @transaction.atomic
    def update_meal(
        *,
        meal,
        meal_name=None,
        meal_time=None,
        foods=None,
        calories=None,
    ):
        """
        Update an existing meal.
        """

        if meal_name is not None:
            if not meal_name:
                raise ValidationError(
                    {
                        "meal_name": (
                            "Meal name cannot be empty."
                        )
                    }
                )

            meal.meal_name = meal_name

        if meal_time is not None:
            if not meal_time:
                raise ValidationError(
                    {
                        "meal_time": (
                            "Meal time cannot be empty."
                        )
                    }
                )

            meal.meal_time = meal_time

        if foods is not None:
            if not foods:
                raise ValidationError(
                    {
                        "foods": (
                            "Foods cannot be empty."
                        )
                    }
                )

            meal.foods = foods

        if calories is not None:
            if calories < 0:
                raise ValidationError(
                    {
                        "calories": (
                            "Calories cannot be negative."
                        )
                    }
                )

            meal.calories = calories

        meal.save()

        return meal

    @staticmethod
    @transaction.atomic
    def delete_meal(
        *,
        meal,
    ):
        """
        Delete a meal.
        """

        meal.delete()

        return True