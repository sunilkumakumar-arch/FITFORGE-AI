from django.urls import include, path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [

   path(
       "token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),

    path( 
        "token/refresh/",
         TokenRefreshView.as_view(),
         name="token_refresh",
    ),

    path(
    "trainer-assignments/",
    include("trainer_assignments.urls")
    ),
    
    path("accounts/", include("accounts.urls")),
    path("memberships/", include("memberships.urls")),
    path("employees/", include("employees.urls")),
    path("attendance/", include("attendance.urls")),
    path("trainers/", include("trainers.urls")),
    path("billing/", include("billing.urls")),
    path("workouts/", include("workouts.urls")),
    path("nutrition/", include("nutrition.urls")),
    path("reports/", include("reports.urls")),
    path("notifications/", include("notifications.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("ai-coach/", include("ai_coach.urls")),
    path("billing/",include("billing.urls")),
    path("pt-packages/",include("pt_packages.urls")),
    path("leads/", include("leads.urls")),
    
   
    
    
    

    
]