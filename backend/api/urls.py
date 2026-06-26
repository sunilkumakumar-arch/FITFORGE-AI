from django.urls import path, include

urlpatterns = [

    path(
        "memberships/",
        include("memberships.urls"),
    ),

]

from django.urls import path, include

urlpatterns = [

    path(
        "accounts/",
        include("accounts.urls"),
    ),

]