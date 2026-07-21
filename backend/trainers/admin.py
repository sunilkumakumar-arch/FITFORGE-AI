from django.contrib import admin

from .models import (
    Trainer,
    TrainerCertification,
    TrainerWeeklyOff,
)


class TrainerCertificationInline(admin.TabularInline):
    model = TrainerCertification
    extra = 1
    autocomplete_fields = ["certification"]


class TrainerWeeklyOffInline(admin.TabularInline):
    model = TrainerWeeklyOff
    extra = 1


@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):

    list_display = (
        "trainer_code",
        "first_name",
        "last_name",
        "specialization",
        "experience_years",
        "trainer_level",
        "trainer_capacity",
        "employment_status",
        "trainer_status",
        "phone",
        "email",
    )

    list_filter = (
        "employment_status",
        "trainer_status",
        "trainer_level",
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

    inlines = [
        TrainerCertificationInline,
        TrainerWeeklyOffInline,
    ]


@admin.register(TrainerCertification)
class TrainerCertificationAdmin(admin.ModelAdmin):

    list_display = (
        "trainer",
        "certification",
        "verification_status",
        "issue_date",
        "expiry_date",
    )

    list_filter = (
        "verification_status",
        "certification",
    )

    search_fields = (
        "trainer__trainer_code",
        "trainer__first_name",
        "trainer__last_name",
        "certification__name",
    )

    autocomplete_fields = [
        "trainer",
        "certification",
    ]

    ordering = (
        "trainer",
    )

    list_per_page = 25


@admin.register(TrainerWeeklyOff)
class TrainerWeeklyOffAdmin(admin.ModelAdmin):

    list_display = (
        "trainer",
        "week_start_date",
        "off_day",
    )

    list_filter = (
        "off_day",
    )

    search_fields = (
        "trainer__trainer_code",
        "trainer__first_name",
        "trainer__last_name",
    )

    autocomplete_fields = [
        "trainer",
    ]

    ordering = (
        "week_start_date",
    )

    list_per_page = 25