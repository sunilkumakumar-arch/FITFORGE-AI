from django.urls import include, path
from rest_framework.routers import DefaultRouter

from workouts.views.exercise_views import ExerciseViewSet
from workouts.views.template_views import (
    WorkoutTemplateViewSet,
    WorkoutDayViewSet,
    WorkoutExerciseViewSet,
)

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

urlpatterns = [
    path("", include(router.urls)),
]