from rest_framework.routers import DefaultRouter

from .views import (
    WorkoutPlanViewSet,
    WorkoutDayViewSet,
    WorkoutExerciseViewSet,
    MemberWorkoutAssignmentViewSet,
)

router = DefaultRouter()

router.register(r"plans", WorkoutPlanViewSet)
router.register(r"days", WorkoutDayViewSet)
router.register(r"exercises", WorkoutExerciseViewSet)
router.register(r"assignments", MemberWorkoutAssignmentViewSet)

urlpatterns = router.urls