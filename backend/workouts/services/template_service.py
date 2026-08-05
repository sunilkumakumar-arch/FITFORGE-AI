from django.db import transaction
from rest_framework.exceptions import ValidationError

from workouts.models import (
    WorkoutTemplate,
    WorkoutDay,
    WorkoutExercise,
    Exercise,
)


class WorkoutTemplateService:
    """
    Business logic for workout templates.
    """

    # =====================================================
    # Create Template
    # =====================================================

    @staticmethod
    @transaction.atomic
    def create_template(
        *,
        name,
        goal,
        difficulty,
        duration_weeks,
        created_by=None,
        description="",
    ):
        if WorkoutTemplate.objects.filter(name=name).exists():
            raise ValidationError(
                {
                    "name": "A workout template with this name already exists."
                }
            )

        return WorkoutTemplate.objects.create(
            name=name,
            goal=goal,
            difficulty=difficulty,
            duration_weeks=duration_weeks,
            created_by=created_by,
            description=description,
        )

    # =====================================================
    # Add Workout Day
    # =====================================================

    @staticmethod
    @transaction.atomic
    def add_workout_day(
        *,
        workout_template,
        day_name,
        focus_area,
        sort_order,
    ):
        return WorkoutDay.objects.create(
            workout_template=workout_template,
            day_name=day_name,
            focus_area=focus_area,
            sort_order=sort_order,
        )

    # =====================================================
    # Add Exercise
    # =====================================================

    @staticmethod
    @transaction.atomic
    def add_exercise(
        *,
        workout_day,
        exercise,
        exercise_order,
        sets,
        reps,
        rest_seconds=60,
        tempo="",
        rpe=None,
        notes="",
    ):
        if not isinstance(exercise, Exercise):
            raise ValidationError(
                {
                    "exercise": "Invalid exercise selected."
                }
            )

        return WorkoutExercise.objects.create(
            workout_day=workout_day,
            exercise=exercise,
            exercise_order=exercise_order,
            sets=sets,
            reps=reps,
            rest_seconds=rest_seconds,
            tempo=tempo,
            rpe=rpe,
            notes=notes,
        )

    # =====================================================
    # Archive Template
    # =====================================================

    @staticmethod
    @transaction.atomic
    def archive_template(workout_template):
        workout_template.is_active = False
        workout_template.save(update_fields=["is_active"])

        return workout_template

    # =====================================================
    # Duplicate Template
    # =====================================================

    @staticmethod
    @transaction.atomic
    def duplicate_template(
        *,
        workout_template,
        new_name,
    ):
        new_template = WorkoutTemplate.objects.create(
            name=new_name,
            goal=workout_template.goal,
            difficulty=workout_template.difficulty,
            duration_weeks=workout_template.duration_weeks,
            description=workout_template.description,
            created_by=workout_template.created_by,
        )

        for day in workout_template.days.all():

            new_day = WorkoutDay.objects.create(
                workout_template=new_template,
                day_name=day.day_name,
                focus_area=day.focus_area,
                sort_order=day.sort_order,
            )

            for exercise in day.exercises.all():

                WorkoutExercise.objects.create(
                    workout_day=new_day,
                    exercise=exercise.exercise,
                    exercise_order=exercise.exercise_order,
                    sets=exercise.sets,
                    reps=exercise.reps,
                    rest_seconds=exercise.rest_seconds,
                    tempo=exercise.tempo,
                    rpe=exercise.rpe,
                    notes=exercise.notes,
                )

        return new_template