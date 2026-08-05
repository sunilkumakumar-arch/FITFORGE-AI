from django.urls import path

from .views import (
    ReceptionMemberDashboardAPIView,
    ReceptionSearchAPIView,
     ReceptionRenewAPIView
)

urlpatterns = [
    path(
        "member/<str:member_code>/",
        ReceptionMemberDashboardAPIView.as_view(),
        name="reception-member-dashboard",
    ),

    path(
        "search/",
        ReceptionSearchAPIView.as_view(),
        name="reception-search",
    ),
    path(
        "member/<str:member_code>/renew/",
        ReceptionRenewAPIView.as_view(),
        name="reception-member-renew",
    ),
]