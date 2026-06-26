from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    MembershipPlanViewSet,
    MemberMembershipViewSet,
)

router = DefaultRouter()

router.register(
    "membership-plans",
    MembershipPlanViewSet
)

router.register(
    "member-memberships",
    MemberMembershipViewSet
)

urlpatterns = [
    path("", include(router.urls)),
]