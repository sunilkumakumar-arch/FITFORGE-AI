from rest_framework.routers import DefaultRouter


from .views import (
    OrganizationViewSet,
    BranchViewSet,
    DepartmentViewSet,
    DesignationViewSet,
)

router = DefaultRouter()

router.register(
    r"organizations",
    OrganizationViewSet,
    basename="organization",
)

router.register(
    r"branches",
    BranchViewSet,
    basename="branch",
)

router.register(
    r"departments",
    DepartmentViewSet,
    basename="department",
)

router.register(
    r"designations",
    DesignationViewSet,
    basename="designation",
)

urlpatterns = router.urls