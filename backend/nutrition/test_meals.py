from django.test import TestCase
from rest_framework.exceptions import ValidationError

from nutrition.models import NutritionPlan, Meal
from nutrition.services.meal_service import NutritionMealService


class NutritionMealServiceTests(TestCase):

    def setUp(self):
        self.nutrition_plan = NutritionPlan.objects.create(
            name="Test Muscle Gain Plan",
            goal="Muscle Gain",
            calories=2500,
            protein=180,
            carbs=280,
            fats=70,
        )

    def test_create_meal_successfully(self):
        meal = NutritionMealService.create_meal(
            nutrition_plan=self.nutrition_plan,
            meal_name="Breakfast",
            meal_time="8:00 AM",
            foods="Eggs, oats and banana",
            calories=600,
        )

        self.assertIsNotNone(meal.id)
        self.assertEqual(meal.nutrition_plan, self.nutrition_plan)
        self.assertEqual(meal.meal_name, "Breakfast")
        self.assertEqual(meal.meal_time, "8:00 AM")
        self.assertEqual(meal.foods, "Eggs, oats and banana")
        self.assertEqual(meal.calories, 600)

    def test_create_meal_rejects_missing_meal_name(self):
        with self.assertRaises(ValidationError):
            NutritionMealService.create_meal(
                nutrition_plan=self.nutrition_plan,
                meal_name="",
                meal_time="8:00 AM",
                foods="Eggs",
                calories=300,
            )

    def test_create_meal_rejects_missing_meal_time(self):
        with self.assertRaises(ValidationError):
            NutritionMealService.create_meal(
                nutrition_plan=self.nutrition_plan,
                meal_name="Breakfast",
                meal_time="",
                foods="Eggs",
                calories=300,
            )

    def test_create_meal_rejects_missing_foods(self):
        with self.assertRaises(ValidationError):
            NutritionMealService.create_meal(
                nutrition_plan=self.nutrition_plan,
                meal_name="Breakfast",
                meal_time="8:00 AM",
                foods="",
                calories=300,
            )

    def test_create_meal_rejects_negative_calories(self):
        with self.assertRaises(ValidationError):
            NutritionMealService.create_meal(
                nutrition_plan=self.nutrition_plan,
                meal_name="Breakfast",
                meal_time="8:00 AM",
                foods="Eggs",
                calories=-100,
            )

    def test_update_meal_successfully(self):
        meal = Meal.objects.create(
            nutrition_plan=self.nutrition_plan,
            meal_name="Breakfast",
            meal_time="8:00 AM",
            foods="Eggs",
            calories=300,
        )

        updated_meal = NutritionMealService.update_meal(
            meal=meal,
            meal_name="High Protein Breakfast",
            meal_time="8:30 AM",
            foods="Eggs, oats and Greek yogurt",
            calories=500,
        )

        updated_meal.refresh_from_db()

        self.assertEqual(
            updated_meal.meal_name,
            "High Protein Breakfast",
        )
        self.assertEqual(
            updated_meal.meal_time,
            "8:30 AM",
        )
        self.assertEqual(
            updated_meal.foods,
            "Eggs, oats and Greek yogurt",
        )
        self.assertEqual(
            updated_meal.calories,
            500,
        )

    def test_update_meal_rejects_negative_calories(self):
        meal = Meal.objects.create(
            nutrition_plan=self.nutrition_plan,
            meal_name="Breakfast",
            meal_time="8:00 AM",
            foods="Eggs",
            calories=300,
        )

        with self.assertRaises(ValidationError):
            NutritionMealService.update_meal(
                meal=meal,
                calories=-100,
            )

    def test_delete_meal_successfully(self):
        meal = Meal.objects.create(
            nutrition_plan=self.nutrition_plan,
            meal_name="Breakfast",
            meal_time="8:00 AM",
            foods="Eggs",
            calories=300,
        )

        result = NutritionMealService.delete_meal(
            meal=meal,
        )

        self.assertTrue(result)

        self.assertFalse(
            Meal.objects.filter(id=meal.id).exists()
        )
