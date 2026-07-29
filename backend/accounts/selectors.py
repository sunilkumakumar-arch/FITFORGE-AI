from django.shortcuts import get_object_or_404

from .models import (
    Member,
    MemberProfile,
    EmergencyContact,
    MedicalProfile,
    FitnessGoal,
    BodyAssessment,
)


class MemberSelector:

    @staticmethod
    def get_queryset():
        return Member.objects.all()

    @staticmethod
    def get_by_id(member_id):
        return get_object_or_404(
            Member,
            pk=member_id,
        )

    @staticmethod
    def get_by_member_code(member_code):
        return get_object_or_404(
            Member,
            member_code=member_code,
        )

    @staticmethod
    def phone_exists(phone, exclude_id=None):
        queryset = Member.objects.filter(phone=phone)

        if exclude_id is not None:
            queryset = queryset.exclude(id=exclude_id)

        return queryset.exists()

    @staticmethod
    def email_exists(email, exclude_id=None):
        if not email:
            return False

        queryset = Member.objects.filter(email=email)

        if exclude_id is not None:
            queryset = queryset.exclude(id=exclude_id)

        return queryset.exists()


class MemberProfileSelector:

    @staticmethod
    def get_queryset():
        return MemberProfile.objects.select_related("member")

    @staticmethod
    def get_by_id(pk):
        return get_object_or_404(
            MemberProfile,
            pk=pk,
        )


class EmergencyContactSelector:

    @staticmethod
    def get_queryset():
        return EmergencyContact.objects.select_related("member")

    @staticmethod
    def get_by_id(pk):
        return get_object_or_404(
            EmergencyContact,
            pk=pk,
        )


class MedicalProfileSelector:

    @staticmethod
    def get_queryset():
        return MedicalProfile.objects.select_related("member")

    @staticmethod
    def get_by_id(pk):
        return get_object_or_404(
            MedicalProfile,
            pk=pk,
        )


class FitnessGoalSelector:

    @staticmethod
    def get_queryset():
        return FitnessGoal.objects.select_related("member")

    @staticmethod
    def get_by_id(pk):
        return get_object_or_404(
            FitnessGoal,
            pk=pk,
        )


class BodyAssessmentSelector:

    @staticmethod
    def get_queryset():
        return BodyAssessment.objects.select_related("member")

    @staticmethod
    def get_by_id(pk):
        return get_object_or_404(
            BodyAssessment,
            pk=pk,
        )