# pt_packages/urls.py

from rest_framework.routers import DefaultRouter

from .views import (
    PTPackageViewSet,
    MemberPTPackageViewSet,
    PTSessionViewSet,
)

router = DefaultRouter()

router.register(
    r"packages",
    PTPackageViewSet,
    basename="pt-package"
)

router.register(
    r"member-packages",
    MemberPTPackageViewSet,
    basename="member-pt-package"
)

router.register(
    r"sessions",
    PTSessionViewSet,
    basename="pt-session"
)

urlpatterns = router.urls