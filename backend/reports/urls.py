from django.urls import path

from .views import BusinessReportView

urlpatterns = [
    path(
        "business/",
        BusinessReportView.as_view(),
        name="business-report"
    ),
]