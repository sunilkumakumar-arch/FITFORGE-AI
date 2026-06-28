from rest_framework.routers import DefaultRouter

from .views import TrainerAssignmentViewSet


router = DefaultRouter()

router.register(
    r"",
    TrainerAssignmentViewSet,
    basename="trainer-assignment"
)

urlpatterns = router.urls