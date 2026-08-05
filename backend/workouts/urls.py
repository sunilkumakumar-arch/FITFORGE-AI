from django.urls import include, path
from rest_framework.routers import DefaultRouter

from workouts.views.exercise_views import ExerciseViewSet
from workouts.views.template_views import (
    WorkoutTemplateViewSet,
    WorkoutDayViewSet,
    WorkoutExerciseViewSet,
)
from workouts.views.assignment_views import MemberWorkoutPlanViewSet
from workouts.views.logging_views import WorkoutLogViewSet

router = DefaultRouter()

router.register(
    r"exercises",
    ExerciseViewSet,
    basename="exercise",
)

router.register(
    r"templates",
    WorkoutTemplateViewSet,
    basename="workout-template",
)

router.register(
    r"days",
    WorkoutDayViewSet,
    basename="workout-day",
)

router.register(
    r"template-exercises",
    WorkoutExerciseViewSet,
    basename="workout-exercise",
)

router.register(
    r"member-plans",
    MemberWorkoutPlanViewSet,
    basename="member-workout-plan",
)

router.register(
    r"logs",
    WorkoutLogViewSet,
    basename="workout-log",
)

urlpatterns = [
    path("", include(router.urls)),
]