from django.contrib import admin
from .models import Certification

@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "issuing_organization",
        "is_active",
    )

    search_fields = (
        "name",
        "issuing_organization",
    )

    list_filter = (
        "is_active",
    )