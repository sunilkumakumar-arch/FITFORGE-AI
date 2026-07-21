from rest_framework.routers import DefaultRouter

from .views import (
    TrainerViewSet,
    TrainerCertificationViewSet,
    TrainerWeeklyOffViewSet,
)

router = DefaultRouter()

router.register(
    r"",
    TrainerViewSet,
    basename="trainer",
)

router.register(
    r"trainer-certifications",
    TrainerCertificationViewSet,
    basename="trainer-certifications",
)

router.register(
    r"weekly-offs",
    TrainerWeeklyOffViewSet,
    basename="trainer-weekly-off",
)

urlpatterns = router.urls