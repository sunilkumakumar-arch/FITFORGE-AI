# leads/urls.py

from rest_framework.routers import DefaultRouter

from .views import (
    LeadViewSet,
    LeadFollowUpViewSet
)

router = DefaultRouter()

router.register(
    r"",
    LeadViewSet,
    basename="lead"
)

router.register(
    r"followups",
    LeadFollowUpViewSet,
    basename="lead-followup"
)

urlpatterns = router.urls