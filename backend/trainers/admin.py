from django.contrib import admin
from .models import Trainer


@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):

    list_display = (
        "trainer_code",
        "first_name",
        "last_name",
        "specialization",
        "experience_years",
        "employment_status",
        "phone",
        "email",
    )

    list_filter = (
        "employment_status",
        "specialization",
    )

    search_fields = (
        "trainer_code",
        "first_name",
        "last_name",
        "phone",
        "email",
    )

    ordering = (
        "trainer_code",
    )

    list_per_page = 25