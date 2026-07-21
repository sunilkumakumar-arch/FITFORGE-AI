from django.urls import path

from roles.views import (
    RoleListCreateAPIView,
    PermissionListAPIView,
    AssignPermissionAPIView,
)

urlpatterns = [

    path(
        "",
        RoleListCreateAPIView.as_view(),
        name="role-list-create",
    ),

    path(
        "permissions/",
        PermissionListAPIView.as_view(),
        name="permission-list",
    ),

    path(
        "<int:role_id>/assign-permissions/",
        AssignPermissionAPIView.as_view(),
        name="assign-permissions",
    ),
]