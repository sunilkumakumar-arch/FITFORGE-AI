from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

from .models import (
    Trainer,
    TrainerWeeklyOff,
    TrainerCertification,
)

from trainer_assignments.models import TrainerAssignment


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

    @extend_schema_field(
        serializers.IntegerField()
    )
    def get_current_members(self, obj):
        return TrainerAssignment.objects.filter(
            trainer=obj,
            is_active=True,
            assignment_type="MEMBERSHIP",
        ).count()

    @extend_schema_field(
        serializers.IntegerField()
    )
    def get_available_capacity(self, obj):
        current = self.get_current_members(obj)

        return max(
            obj.trainer_capacity - current,
            0,
        )

    @extend_schema_field(
        serializers.IntegerField()
    )
    def get_pt_clients(self, obj):
        return TrainerAssignment.objects.filter(
            trainer=obj,
            is_active=True,
            assignment_type="PT",
        ).count()

    @extend_schema_field(
        serializers.CharField(
            allow_null=True
        )
    )
    def get_weekly_off(self, obj):
        weekly_off = (
            TrainerWeeklyOff.objects
            .filter(
                trainer=obj
            )
            .order_by(
                "-week_start_date"
            )
            .first()
        )

        return (
            weekly_off.off_day
            if weekly_off
            else None
        )

    @extend_schema_field(
        serializers.ListField()
    )
    def get_certifications(self, obj):
        certifications = (
            TrainerCertification.objects
            .filter(
                trainer=obj
            )
            .select_related(
                "certification"
            )
        )

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
            Trainer.objects
            .filter(phone=value)
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
            Trainer.objects
            .filter(email=value)
            .exclude(id=trainer_id)
            .exists()
        ):
            raise serializers.ValidationError(
                "Email already exists."
            )

        return value


class TrainerWeeklyOffSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = TrainerWeeklyOff
        fields = "__all__"


class TrainerCertificationSerializer(
    serializers.ModelSerializer
):

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


class TrainerCreateSerializer(
    serializers.Serializer
):

    first_name = serializers.CharField(
        max_length=100
    )

    last_name = serializers.CharField(
        max_length=100
    )

    phone = serializers.CharField(
        max_length=15
    )

    email = serializers.EmailField(
        required=False,
        allow_blank=True,
    )

    specialization = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    experience_years = serializers.IntegerField(
        default=0
    )

    trainer_level = serializers.ChoiceField(
        choices=Trainer.TRAINER_LEVELS,
        default="LEVEL_1",
    )

    trainer_capacity = serializers.IntegerField(
        default=40
    )

    shift_type = serializers.ChoiceField(
        choices=Trainer.SHIFT_CHOICES,
        default="SHIFT_3",
    )

    salary = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    employment_status = serializers.ChoiceField(
        choices=Trainer.EMPLOYMENT_STATUS,
        default="Active",
    )

    def create(self, validated_data):

        from .services import TrainerService

        return TrainerService.create_trainer(
            validated_data
        )