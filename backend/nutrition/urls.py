from rest_framework.routers import DefaultRouter

from .views import (
    NutritionPlanViewSet,
    MealViewSet,
    MemberNutritionAssignmentViewSet,
)

router = DefaultRouter()

router.register(r"plans", NutritionPlanViewSet)
router.register(r"meals", MealViewSet)
router.register(r"assignments", MemberNutritionAssignmentViewSet)

urlpatterns = router.urls