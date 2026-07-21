from rest_framework import serializers

from .models import (
    Trainer,
    TrainerWeeklyOff,
)

from trainer_assignments.models import TrainerAssignment
from .models import TrainerCertification


class TrainerSerializer(serializers.ModelSerializer):

    current_members = serializers.SerializerMethodField()
    available_capacity = serializers.SerializerMethodField()
    pt_clients = serializers.SerializerMethodField()
    weekly_off = serializers.SerializerMethodField()
    certifications = serializers.SerializerMethodField()

    class Meta:
        model = Trainer
        fields = [
            "id",
            "trainer_code",
            "first_name",
            "last_name",
            "phone",
            "email",
            "specialization",
            "experience_years",
            "trainer_level",
            "trainer_capacity",
            "shift_type",
            "trainer_status",
            "employment_status",
            "joining_date",
            "salary",
            "photo",
            "created_at",
            "updated_at",
            "current_members",
            "available_capacity",
            "pt_clients",
            "weekly_off",
            "certifications",
        ]

    def get_current_members(self, obj):
        return TrainerAssignment.objects.filter(
            trainer=obj,
            is_active=True,
            assignment_type="MEMBERSHIP",
        ).count()

    def get_available_capacity(self, obj):
        current = self.get_current_members(obj)
        return max(obj.trainer_capacity - current, 0)

    def get_pt_clients(self, obj):
        return TrainerAssignment.objects.filter(
            trainer=obj,
            is_active=True,
            assignment_type="PT",
        ).count()

    def get_weekly_off(self, obj):
        weekly_off = (
            TrainerWeeklyOff.objects.filter(
                trainer=obj
            )
            .order_by("-week_start_date")
            .first()
        )

        return weekly_off.off_day if weekly_off else None
    
    def get_certifications(self, obj):
        certifications = TrainerCertification.objects.filter(
            trainer=obj
        ).select_related("certification")

        return TrainerCertificationSerializer(
            certifications,
            many=True,
            context=self.context,
        ).data

    def validate_phone(self, value):

        trainer_id = (
            self.instance.id
            if self.instance
            else None
        )

        if (
            Trainer.objects.filter(phone=value)
            .exclude(id=trainer_id)
            .exists()
        ):
            raise serializers.ValidationError(
                "Phone number already exists."
            )

        return value

    def validate_email(self, value):

        if not value:
            return value

        trainer_id = (
            self.instance.id
            if self.instance
            else None
        )

        if (
            Trainer.objects.filter(email=value)
            .exclude(id=trainer_id)
            .exists()
        ):
            raise serializers.ValidationError(
                "Email already exists."
            )

        return value


class TrainerWeeklyOffSerializer(serializers.ModelSerializer):

    class Meta:
        model = TrainerWeeklyOff
        fields = "__all__"


class TrainerCertificationSerializer(serializers.ModelSerializer):

    certification_name = serializers.CharField(
        source="certification.name",
        read_only=True,
    )

    class Meta:
        model = TrainerCertification

        fields = (
            "id",
            "trainer",
            "certification",
            "certification_name",
            "certificate_number",
            "issue_date",
            "expiry_date",
            "certificate_file",
            "verification_status",
            "created_at",
        )

        read_only_fields = (
            "created_at",
        )