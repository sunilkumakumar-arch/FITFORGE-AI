from django.test import TestCase
from rest_framework.exceptions import ValidationError

from trainers.models import Trainer
from workouts.models import (
    MuscleGroup,
    ExerciseCategory,
    Equipment,
    Exercise,
    WorkoutTemplate,
    WorkoutDay,
    WorkoutExercise,
)
from workouts.services.template_service import WorkoutTemplateService


class WorkoutTemplateServiceTests(TestCase):

    def setUp(self):
        self.trainer = Trainer.objects.create(
            first_name="Template",
            last_name="Trainer",
            phone="9999992001",
            email="template.trainer@example.com",
            employment_status="Active",
        )

        self.muscle_group = MuscleGroup.objects.create(
            name="Chest",
            description="Chest muscles",
        )

        self.category = ExerciseCategory.objects.create(
            name="Push",
            description="Push exercises",
        )

        self.equipment = Equipment.objects.create(
            name="Barbell",
            description="Olympic barbell",
        )

        self.exercise = Exercise.objects.create(
            name="Bench Press",
            muscle_group=self.muscle_group,
            category=self.category,
            equipment=self.equipment,
            difficulty="INTERMEDIATE",
            instructions="Press the bar upward.",
        )

        self.template = WorkoutTemplate.objects.create(
            name="Template Test Workout",
            goal="MUSCLE_GAIN",
            difficulty="INTERMEDIATE",
            duration_weeks=8,
            created_by=self.trainer,
            description="Template service test.",
        )

    def test_create_template_successfully(self):
        template = WorkoutTemplateService.create_template(
            name="New Workout Template",
            goal="STRENGTH",
            difficulty="ADVANCED",
            duration_weeks=6,
            created_by=self.trainer,
            description="Strength template.",
        )

        self.assertIsNotNone(template.id)
        self.assertEqual(template.name, "New Workout Template")
        self.assertEqual(template.goal, "STRENGTH")
        self.assertEqual(template.difficulty, "ADVANCED")
        self.assertEqual(template.duration_weeks, 6)
        self.assertEqual(template.created_by, self.trainer)

    def test_create_template_rejects_duplicate_name(self):
        with self.assertRaises(ValidationError):
            WorkoutTemplateService.create_template(
                name="Template Test Workout",
                goal="STRENGTH",
                difficulty="BEGINNER",
                duration_weeks=4,
                created_by=self.trainer,
            )

    def test_add_workout_day_successfully(self):
        day = WorkoutTemplateService.add_workout_day(
            workout_template=self.template,
            day_name="MONDAY",
            focus_area="Chest",
            sort_order=1,
        )

        self.assertIsNotNone(day.id)
        self.assertEqual(day.workout_template, self.template)
        self.assertEqual(day.day_name, "MONDAY")
        self.assertEqual(day.focus_area, "Chest")
        self.assertEqual(day.sort_order, 1)

    def test_add_exercise_successfully(self):
        day = WorkoutTemplateService.add_workout_day(
            workout_template=self.template,
            day_name="MONDAY",
            focus_area="Chest",
            sort_order=1,
        )

        workout_exercise = WorkoutTemplateService.add_exercise(
            workout_day=day,
            exercise=self.exercise,
            exercise_order=1,
            sets=4,
            reps="8-10",
            rest_seconds=90,
            tempo="3-1-1",
            rpe=8,
            notes="Controlled movement.",
        )

        self.assertIsNotNone(workout_exercise.id)
        self.assertEqual(
            workout_exercise.workout_day,
            day,
        )
        self.assertEqual(
            workout_exercise.exercise,
            self.exercise,
        )
        self.assertEqual(workout_exercise.sets, 4)
        self.assertEqual(workout_exercise.reps, "8-10")
        self.assertEqual(workout_exercise.rest_seconds, 90)
        self.assertEqual(workout_exercise.tempo, "3-1-1")
        self.assertEqual(workout_exercise.rpe, 8)

    def test_add_exercise_rejects_invalid_exercise(self):
        day = WorkoutTemplateService.add_workout_day(
            workout_template=self.template,
            day_name="MONDAY",
            focus_area="Chest",
            sort_order=1,
        )

        with self.assertRaises(ValidationError):
            WorkoutTemplateService.add_exercise(
                workout_day=day,
                exercise="Invalid Exercise",
                exercise_order=1,
                sets=3,
                reps="10",
            )

    def test_archive_template(self):
        archived = WorkoutTemplateService.archive_template(
            self.template
        )

        self.assertFalse(archived.is_active)

    def test_duplicate_template_copies_days_and_exercises(self):
        day1 = WorkoutTemplateService.add_workout_day(
            workout_template=self.template,
            day_name="MONDAY",
            focus_area="Chest",
            sort_order=1,
        )

        day2 = WorkoutTemplateService.add_workout_day(
            workout_template=self.template,
            day_name="WEDNESDAY",
            focus_area="Back",
            sort_order=2,
        )

        WorkoutTemplateService.add_exercise(
            workout_day=day1,
            exercise=self.exercise,
            exercise_order=1,
            sets=4,
            reps="8-10",
            rest_seconds=90,
            tempo="3-1-1",
            rpe=8,
            notes="Chest exercise.",
        )

        WorkoutTemplateService.add_exercise(
            workout_day=day2,
            exercise=self.exercise,
            exercise_order=1,
            sets=3,
            reps="10-12",
            rest_seconds=60,
            notes="Back exercise.",
        )

        duplicated = WorkoutTemplateService.duplicate_template(
            workout_template=self.template,
            new_name="Duplicated Workout Template",
        )

        self.assertIsNotNone(duplicated.id)
        self.assertNotEqual(
            duplicated.id,
            self.template.id,
        )

        self.assertEqual(
            duplicated.name,
            "Duplicated Workout Template",
        )

        self.assertEqual(
            duplicated.goal,
            self.template.goal,
        )

        self.assertEqual(
            duplicated.difficulty,
            self.template.difficulty,
        )

        duplicated_days = duplicated.days.all().order_by(
            "sort_order"
        )

        self.assertEqual(
            duplicated_days.count(),
            2,
        )

        self.assertEqual(
            list(
                duplicated_days.values_list(
                    "day_name",
                    flat=True,
                )
            ),
            [
                "MONDAY",
                "WEDNESDAY",
            ],
        )

        self.assertEqual(
            WorkoutExercise.objects.filter(
                workout_day__workout_template=duplicated
            ).count(),
            2,
        )

        self.assertEqual(
            WorkoutExercise.objects.filter(
                workout_day__workout_template=self.template
            ).count(),
            2,
        )

    def test_duplicate_template_does_not_modify_original(self):
        day = WorkoutTemplateService.add_workout_day(
            workout_template=self.template,
            day_name="FRIDAY",
            focus_area="Legs",
            sort_order=1,
        )

        WorkoutTemplateService.add_exercise(
            workout_day=day,
            exercise=self.exercise,
            exercise_order=1,
            sets=4,
            reps="8-10",
        )

        duplicated = WorkoutTemplateService.duplicate_template(
            workout_template=self.template,
            new_name="Independent Copy",
        )

        duplicated_day = duplicated.days.first()

        self.assertNotEqual(
            duplicated_day.id,
            day.id,
        )

        duplicated_exercise = duplicated_day.exercises.first()

        original_exercise = day.exercises.first()

        self.assertNotEqual(
            duplicated_exercise.id,
            original_exercise.id,
        )

        self.assertEqual(
            duplicated_exercise.exercise,
            original_exercise.exercise,
        )