from django.urls import path

from .views import (
    AssignTrainerAPIView,
    AutoAssignTrainerAPIView,
    ChangeTrainerAPIView,
    MemberAssignmentAPIView,
    TrainerHistoryAPIView,
)

app_name = "general_training"

urlpatterns = [

    # ---------------------------------------
    # Assignment APIs
    # ---------------------------------------

    path(
        "assign/",
        AssignTrainerAPIView.as_view(),
        name="assign-trainer",
    ),

    path(
        "auto-assign/",
        AutoAssignTrainerAPIView.as_view(),
        name="auto-assign-trainer",
    ),

    path(
        "change-trainer/",
        ChangeTrainerAPIView.as_view(),
        name="change-trainer",
    ),

    # ---------------------------------------
    # Query APIs
    # ---------------------------------------

    path(
        "member/<int:member_id>/",
        MemberAssignmentAPIView.as_view(),
        name="member-assignment",
    ),

    path(
        "history/<int:member_id>/",
        TrainerHistoryAPIView.as_view(),
        name="trainer-history",
    ),
]