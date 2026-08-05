from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    PTPackageViewSet,
    MemberPTPackageViewSet,
    PTSessionViewSet,
    PTPackagePurchaseAPIView,
    PTAssignTrainerAPIView,
)

router = DefaultRouter()

router.register(
    r"packages",
    PTPackageViewSet,
    basename="pt-package",
)

router.register(
    r"member-packages",
    MemberPTPackageViewSet,
    basename="member-pt-package",
)

router.register(
    r"sessions",
    PTSessionViewSet,
    basename="pt-session",
)

urlpatterns = [
    path(
        "purchase/",
        PTPackagePurchaseAPIView.as_view(),
        name="pt-package-purchase",
    ),
    path(
        "assign-trainer/",
        PTAssignTrainerAPIView.as_view(),
        name="pt-package-assign-trainer",
    ),
]

urlpatterns += router.urls