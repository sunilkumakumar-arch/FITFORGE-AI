from django.contrib import admin

from workouts.models import (
    Exercise,
    ExerciseCategory,
    ExerciseMedia,
    Equipment,
    MuscleGroup,
)


@admin.register(MuscleGroup)
class MuscleGroupAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "display_order",
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
    )


@admin.register(ExerciseCategory)
class ExerciseCategoryAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
    )


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
    )


class ExerciseMediaInline(admin.TabularInline):
    model = ExerciseMedia
    extra = 0


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "muscle_group",
        "category",
        "difficulty",
        "equipment",
        "is_active",
    )

    list_filter = (
        "muscle_group",
        "category",
        "difficulty",
        "is_active",
    )

    search_fields = (
        "name",
        "description",
    )

    inlines = [
        ExerciseMediaInline,
    ]


@admin.register(ExerciseMedia)
class ExerciseMediaAdmin(admin.ModelAdmin):

    list_display = (
        "exercise",
        "media_type",
        "display_order",
    )

    list_filter = (
        "media_type",
    )