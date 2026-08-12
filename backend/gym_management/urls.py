from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    GymFacilityViewSet,
    GymZoneViewSet,
    EquipmentViewSet,
    EquipmentMaintenanceViewSet,
)


router = DefaultRouter()

router.register(
    r"facilities",
    GymFacilityViewSet,
    basename="gym-facility",
)

router.register(
    r"zones",
    GymZoneViewSet,
    basename="gym-zone",
)

router.register(
    r"equipment",
    EquipmentViewSet,
    basename="equipment",
)

router.register(
    r"maintenance",
    EquipmentMaintenanceViewSet,
    basename="equipment-maintenance",
)


urlpatterns = [
    path(
        "",
        include(router.urls),
    ),
]