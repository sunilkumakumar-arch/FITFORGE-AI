from django.urls import path

from .views import (
    LoginView,
    ChangePasswordView,
    CurrentUserView,
    LogoutView,
)

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path(
        "change-password/",
        ChangePasswordView.as_view(),
        name="change-password",
    ),

    path(
        "me/",
        CurrentUserView.as_view(),
        name="current-user",
    ),

    path(
        "logout/",
        LogoutView.as_view(),
        name="logout",
    ),
]