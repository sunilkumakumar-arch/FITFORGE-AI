from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field


class ReceptionDashboardSerializer(serializers.Serializer):
    """
    Serializer for the Reception Dashboard.
    """

    success = serializers.BooleanField()

    member = serializers.SerializerMethodField()

    member_hub = serializers.SerializerMethodField()

    membership = serializers.SerializerMethodField()

    attendance = serializers.SerializerMethodField()

    trainer_assignment = serializers.SerializerMethodField()

    pt_package = serializers.SerializerMethodField()

    # ======================================================
    # MEMBER
    # ======================================================

    @extend_schema_field(
        serializers.DictField(allow_null=True)
    )
    def get_member(self, obj):

        member = obj.get("member")

        if not member:
            return None

        return {
            "id": member.id,
            "member_code": member.member_code,
            "first_name": member.first_name,
            "last_name": member.last_name,
            "phone": member.phone,
            "email": member.email,
        }

    # ======================================================
    # MEMBER HUB
    # ======================================================

    @extend_schema_field(
        serializers.DictField(allow_null=True)
    )
    def get_member_hub(self, obj):

        hub = obj.get("member_hub")

        if not hub:
            return None

        return {
            "public_member_id": hub.public_member_id,
            "card_level": hub.card_level,
            "card_version": hub.card_version,
            "qr_code": (
                hub.qr_code.url
                if hub.qr_code
                else None
            ),
        }

    # ======================================================
    # MEMBERSHIP
    # ======================================================

    @extend_schema_field(
        serializers.DictField(allow_null=True)
    )
    def get_membership(self, obj):

        membership = obj.get("membership")

        if not membership:
            return None

        return {
            "plan": membership.plan.name,
            "status": membership.status,
            "start_date": membership.start_date,
            "end_date": membership.end_date,
            "remaining_days": (
                membership.remaining_days
            ),
        }

    # ======================================================
    # ATTENDANCE
    # ======================================================

    @extend_schema_field(
        serializers.DictField(allow_null=True)
    )
    def get_attendance(self, obj):

        attendance = obj.get("attendance")

        if not attendance:
            return None

        return {
            "attendance_date": (
                attendance.attendance_date
            ),
            "check_in": attendance.check_in,
            "check_out": attendance.check_out,
            "status": attendance.status,
            "method": attendance.checkin_method,
        }

    # ======================================================
    # TRAINER ASSIGNMENT
    # ======================================================

    @extend_schema_field(
        serializers.DictField(allow_null=True)
    )
    def get_trainer_assignment(self, obj):

        assignment = obj.get(
            "trainer_assignment"
        )

        if not assignment:
            return None

        return {
            "trainer_name": (
                f"{assignment.trainer.first_name} "
                f"{assignment.trainer.last_name}"
            ),
            "sessions_per_week": (
                assignment.sessions_per_week
            ),
            "monthly_fee": (
                assignment.monthly_fee
            ),
        }

    # ======================================================
    # PT PACKAGE
    # ======================================================

    @extend_schema_field(
        serializers.DictField(allow_null=True)
    )
    def get_pt_package(self, obj):

        package = obj.get("pt_package")

        if not package:
            return None

        return {
            "id": package.id,
        }


# ==========================================================
# MEMBERSHIP RENEWAL
# ==========================================================


class MembershipRenewSerializer(serializers.Serializer):
    """
    Validates Membership Renewal requests.
    """

    membership_plan_id = serializers.IntegerField()

    amount_paid = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    payment_method = serializers.ChoiceField(
        choices=[
            "Cash",
            "UPI",
            "Card",
            "Bank Transfer",
        ]
    )

    transaction_id = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=100,
    )