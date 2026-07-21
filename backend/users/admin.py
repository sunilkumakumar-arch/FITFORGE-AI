from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "phone_verified",
        "must_change_password",
        "account_locked",
    )

    list_filter = (
        "phone_verified",
        "must_change_password",
        "account_locked",
    )

    search_fields = (
        "user__username",
        "user__email",
    )