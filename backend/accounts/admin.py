from django.contrib import admin
from .models import (
    Member,
    MemberProfile,
    EmergencyContact,
    MedicalProfile,
    FitnessGoal,
    BodyAssessment,
)


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "phone", "email")
    search_fields = ("first_name", "last_name", "phone", "email")


@admin.register(MemberProfile)
class MemberProfileAdmin(admin.ModelAdmin):
    list_display = ("member", "member_code", "city", "country")
    search_fields = ("member__first_name", "member__last_name", "member_code")


@admin.register(EmergencyContact)
class EmergencyContactAdmin(admin.ModelAdmin):
    list_display = ("member", "contact_name", "relationship", "phone")
    search_fields = ("contact_name", "phone")


@admin.register(MedicalProfile)
class MedicalProfileAdmin(admin.ModelAdmin):
    list_display = (
        "member",
        "blood_group",
        "parq_completed",
        "medical_clearance",
    )
    list_filter = (
        "parq_completed",
        "medical_clearance",
    )


@admin.register(FitnessGoal)
class FitnessGoalAdmin(admin.ModelAdmin):
    list_display = (
        "member",
        "primary_goal",
        "target_date",
    )
    list_filter = ("primary_goal",)


@admin.register(BodyAssessment)
class BodyAssessmentAdmin(admin.ModelAdmin):
    list_display = (
        "member",
        "assessment_date",
        "weight",
        "body_fat_percentage",
    )
    list_filter = ("assessment_date",)