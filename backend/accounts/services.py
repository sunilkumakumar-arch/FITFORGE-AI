import re
from django.db import transaction
from django.db.models import Max

from .models import (
    Member,
    MemberProfile,
    EmergencyContact,
    MedicalProfile,
    FitnessGoal,
    BodyAssessment,
)


class MemberService:

    MEMBER_PREFIX = "MBR"

    @classmethod
    def _get_next_sequence(cls):
        """
        Returns the next sequential member number based on the
        highest existing member_code.
        """

        last_member = (
            Member.objects.exclude(member_code="")
            .order_by("-member_code")
            .first()
        )

        if not last_member:
            return 1

        match = re.search(r"(\d+)$", last_member.member_code)

        if not match:
            return 1

        return int(match.group(1)) + 1

    @classmethod
    def _generate_member_code(cls):
        """
        Generates codes like:
        MBR000001
        """

        sequence = cls._get_next_sequence()

        return f"{cls.MEMBER_PREFIX}{sequence:06d}"

    @classmethod
    @transaction.atomic
    def create_member(cls, validated_data):
        """
        Creates a new member with an auto-generated member code.
        """

        validated_data["member_code"] = cls._generate_member_code()

        return Member.objects.create(**validated_data)

    @classmethod
    @transaction.atomic
    def update_member(cls, member, validated_data):
        """
        Updates an existing member.
        """

        for field, value in validated_data.items():
            setattr(member, field, value)

        member.save()

        return member

    @classmethod
    @transaction.atomic
    def delete_member(cls, member):
        """
        Deletes a member.
        """

        member.delete()

    @classmethod
    @transaction.atomic
    def assign_member_code(cls, member):
        """
        Assigns a member code only if one does not already exist.
        Useful for backfilling legacy records.
        """

        if member.member_code:
            return member

        member.member_code = cls._generate_member_code()
        member.save(update_fields=["member_code"])

        return member


class MemberProfileService:

    @staticmethod
    @transaction.atomic
    def create(validated_data):
        return MemberProfile.objects.create(**validated_data)

    @staticmethod
    @transaction.atomic
    def update(instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)

        instance.save()

        return instance

    @staticmethod
    @transaction.atomic
    def delete(instance):
        instance.delete()


class EmergencyContactService:

    @staticmethod
    @transaction.atomic
    def create(validated_data):
        return EmergencyContact.objects.create(**validated_data)

    @staticmethod
    @transaction.atomic
    def update(instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)

        instance.save()

        return instance

    @staticmethod
    @transaction.atomic
    def delete(instance):
        instance.delete()


class MedicalProfileService:

    @staticmethod
    @transaction.atomic
    def create(validated_data):
        return MedicalProfile.objects.create(**validated_data)

    @staticmethod
    @transaction.atomic
    def update(instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)

        instance.save()

        return instance

    @staticmethod
    @transaction.atomic
    def delete(instance):
        instance.delete()


class FitnessGoalService:

    @staticmethod
    @transaction.atomic
    def create(validated_data):
        return FitnessGoal.objects.create(**validated_data)

    @staticmethod
    @transaction.atomic
    def update(instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)

        instance.save()

        return instance

    @staticmethod
    @transaction.atomic
    def delete(instance):
        instance.delete()


class BodyAssessmentService:

    @staticmethod
    @transaction.atomic
    def create(validated_data):
        return BodyAssessment.objects.create(**validated_data)

    @staticmethod
    @transaction.atomic
    def update(instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)

        instance.save()

        return instance

    @staticmethod
    @transaction.atomic
    def delete(instance):
        instance.delete()