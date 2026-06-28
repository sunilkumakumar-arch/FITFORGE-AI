from django.urls import path

from .views import (
    GenerateWorkoutView,
    GenerateNutritionView,
    PostureAssessmentView,
)

urlpatterns = [
    path(
        "workout/",
        GenerateWorkoutView.as_view(),
    ),

    path(
        "nutrition/",
        GenerateNutritionView.as_view(),
    ),

    path(
        "posture/",
        PostureAssessmentView.as_view(),
    ),
]