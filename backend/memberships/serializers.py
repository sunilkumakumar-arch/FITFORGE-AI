from decimal import Decimal

from django.utils import timezone
from rest_framework import serializers

from .models import (
    MembershipPlan,
    MemberMembership,
)


class MembershipPlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = MembershipPlan

        fields = [
            "id",
            "name",
            "code",
            "organization",
            "branch",
            "duration_days",
            "price",
            "joining_fee",
            "freeze_days_allowed",
            "pt_sessions_included",
            "description",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )

    def validate_name(self, value):
        value = value.strip()

        if len(value) < 3:
            raise serializers.ValidationError(
                "Membership plan name must contain at least 3 characters."
            )

        return value

    def validate_code(self, value):
        value = value.strip().upper()

        if len(value) < 2:
            raise serializers.ValidationError(
                "Membership plan code must contain at least 2 characters."
            )

        return value

    def validate_duration_days(self, value):

        if value <= 0:
            raise serializers.ValidationError(
                "Membership duration must be greater than zero."
            )

        if value > 3650:
            raise serializers.ValidationError(
                "Membership duration cannot exceed 3650 days."
            )

        return value

    def validate_price(self, value):

        if value < Decimal("0"):
            raise serializers.ValidationError(
                "Membership price cannot be negative."
            )

        return value

    def validate_joining_fee(self, value):

        if value < Decimal("0"):
            raise serializers.ValidationError(
                "Joining fee cannot be negative."
            )

        return value

    def validate_freeze_days_allowed(self, value):

        if value < 0:
            raise serializers.ValidationError(
                "Freeze days cannot be negative."
            )

        return value

    def validate_pt_sessions_included(self, value):

        if value < 0:
            raise serializers.ValidationError(
                "PT sessions cannot be negative."
            )

        return value

    def validate_description(self, value):
        return value.strip()

    def validate(self, attrs):

        organization = attrs.get(
            "organization",
            getattr(
                self.instance,
                "organization",
                None,
            )
            if self.instance
            else None,
        )

        branch = attrs.get(
            "branch",
            getattr(
                self.instance,
                "branch",
                None,
            )
            if self.instance
            else None,
        )

        if branch and organization:
            if branch.organization_id != organization.id:
                raise serializers.ValidationError(
                    {
                        "branch": (
                            "Selected branch does not belong "
                            "to the selected organization."
                        )
                    }
                )

        return attrs


class MemberMembershipSerializer(
    serializers.ModelSerializer
):

    member_name = serializers.SerializerMethodField()

    plan_name = serializers.SerializerMethodField()

    remaining_days = serializers.ReadOnlyField()

    class Meta:
        model = MemberMembership

        fields = [
            "id",
            "member",
            "member_name",
            "plan",
            "plan_name",
            "start_date",
            "end_date",
            "status",
            "amount_paid",
            "payment_reference",
            "remaining_days",
            "created_at",
            "updated_at",
        ]

        read_only_fields = (
            "id",
            "member_name",
            "plan_name",
            "remaining_days",
            "created_at",
            "updated_at",
        )

    def get_member_name(self, obj):
        return (
            f"{obj.member.first_name} "
            f"{obj.member.last_name}"
        ).strip()

    def get_plan_name(self, obj):
        return obj.plan.name

    def validate_amount_paid(self, value):

        if value < Decimal("0"):
            raise serializers.ValidationError(
                "Amount paid cannot be negative."
            )

        return value

    def validate_payment_reference(self, value):
        return value.strip()

    def validate(self, attrs):

        member = attrs.get(
            "member",
            getattr(
                self.instance,
                "member",
                None,
            )
            if self.instance
            else None,
        )

        plan = attrs.get(
            "plan",
            getattr(
                self.instance,
                "plan",
                None,
            )
            if self.instance
            else None,
        )

        status = attrs.get(
            "status",
            getattr(
                self.instance,
                "status",
                None,
            )
            if self.instance
            else None,
        )

        start_date = attrs.get(
            "start_date",
            getattr(
                self.instance,
                "start_date",
                None,
            )
            if self.instance
            else None,
        )

        end_date = attrs.get(
            "end_date",
            getattr(
                self.instance,
                "end_date",
                None,
            )
            if self.instance
            else None,
        )

        # -------------------------------------------------
        # DATE VALIDATION
        # -------------------------------------------------

        if start_date and end_date:

            if end_date < start_date:
                raise serializers.ValidationError(
                    {
                        "end_date": (
                            "End date cannot be before "
                            "the start date."
                        )
                    }
                )

        # -------------------------------------------------
        # PLAN VALIDATION
        # -------------------------------------------------

        if plan and not plan.is_active:
            raise serializers.ValidationError(
                {
                    "plan": (
                        "Cannot assign an inactive "
                        "membership plan."
                    )
                }
            )

        # -------------------------------------------------
        # ACTIVE MEMBERSHIP VALIDATION
        # -------------------------------------------------

        if member and status == "Active":

            active_memberships = (
                MemberMembership.objects
                .filter(
                    member=member,
                    status="Active",
                )
            )

            if self.instance:

                active_memberships = (
                    active_memberships.exclude(
                        id=self.instance.id
                    )
                )

            if active_memberships.exists():

                raise serializers.ValidationError(
                    {
                        "member": (
                            "Member already has an active "
                            "membership. Please expire, "
                            "renew, or upgrade the existing "
                            "membership first."
                        )
                    }
                )

        return attrs