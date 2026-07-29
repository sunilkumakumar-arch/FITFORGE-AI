from rest_framework import serializers

from .models import (
    Member,
    MemberProfile,
    EmergencyContact,
    MedicalProfile,
    FitnessGoal,
    BodyAssessment,
)

from .selectors import MemberSelector


class MemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = Member
        fields = "__all__"
        read_only_fields = (
            "member_code",
        )

    def validate_phone(self, value):
        member_id = self.instance.id if self.instance else None

        if MemberSelector.phone_exists(value, exclude_id=member_id):
            raise serializers.ValidationError(
                "Mobile number already exists."
            )

        return value

    def validate_email(self, value):
        if not value:
            return value

        member_id = self.instance.id if self.instance else None

        if MemberSelector.email_exists(value, exclude_id=member_id):
            raise serializers.ValidationError(
                "Email already exists."
            )

        return value


class MemberProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberProfile
        fields = "__all__"


class EmergencyContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyContact
        fields = "__all__"


class MedicalProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalProfile
        fields = "__all__"


class FitnessGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = FitnessGoal
        fields = "__all__"


class BodyAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BodyAssessment
        fields = "__all__"