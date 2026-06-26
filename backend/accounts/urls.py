from rest_framework.routers import DefaultRouter
from .views import (
    MemberViewSet,
    MemberProfileViewSet,
    EmergencyContactViewSet,
    MedicalProfileViewSet,
    FitnessGoalViewSet,
    BodyAssessmentViewSet,
)

router = DefaultRouter()

router.register(r"members", MemberViewSet)
router.register(r"member-profiles", MemberProfileViewSet)
router.register(r"emergency-contacts", EmergencyContactViewSet)
router.register(r"medical-profiles", MedicalProfileViewSet)
router.register(r"fitness-goals", FitnessGoalViewSet)
router.register(r"body-assessments", BodyAssessmentViewSet)

urlpatterns = router.urls