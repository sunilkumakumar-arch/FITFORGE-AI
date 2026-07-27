from django.urls import path

from .views import BootstrapInstallAPIView

urlpatterns = [
    path(
        "install/",
        BootstrapInstallAPIView.as_view(),
        name="bootstrap-install",
    ),
]