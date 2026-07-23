from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .purchase_views import MembershipPurchaseView

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
    path(
        "purchase/",
        MembershipPurchaseView.as_view(),
        name="membership-purchase",
    ),

    path(
        "",
        include(router.urls),
    ),
]