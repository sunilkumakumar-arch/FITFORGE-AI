from django.urls import path

from .views import (
    MemberHubByMemberCodeView,
    MemberHubByPublicIdView,
    MemberHubDetailView,
    MemberHubListView,
    QRVerificationView,
)

app_name = "member_hub"

urlpatterns = [
    path(
        "",
        MemberHubListView.as_view(),
        name="member-hub-list",
    ),

    path(
        "verify/",
        QRVerificationView.as_view(),
        name="memberhub-verify",
    ),
    path(
        "<int:pk>/",
        MemberHubDetailView.as_view(),
        name="member-hub-detail",
    ),
    path(
        "public/<str:public_member_id>/",
        MemberHubByPublicIdView.as_view(),
        name="member-hub-public-id",
    ),
    path(
        "member/<str:member_code>/",
        MemberHubByMemberCodeView.as_view(),
        name="member-hub-member-code",
    ),
]