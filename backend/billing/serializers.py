from decimal import Decimal

from rest_framework import serializers

from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):

    member_name = serializers.SerializerMethodField()
    membership_name = serializers.SerializerMethodField()
    organization_name = serializers.SerializerMethodField()
    branch_name = serializers.SerializerMethodField()
    collected_by_name = serializers.SerializerMethodField()

    class Meta:
        model = Payment

        fields = [
            "id",

            # Payment Identification
            "payment_number",
            "invoice_number",
            "receipt_number",

            # Organization
            "organization",
            "organization_name",
            "branch",
            "branch_name",

            # Member
            "member",
            "member_name",
            "membership",
            "membership_name",

            # Employee
            "collected_by",
            "collected_by_name",

            # Financial
            "amount",
            "discount",
            "tax",
            "final_amount",

            # Payment
            "payment_method",
            "payment_status",
            "payment_date",
            "transaction_id",
            "notes",

            # System
            "created_at",
            "updated_at",
        ]

        read_only_fields = (
            "id",
            "payment_number",
            "invoice_number",
            "receipt_number",
            "final_amount",
            "created_at",
            "updated_at",
        )

    def get_member_name(self, obj):
        return (
            f"{obj.member.first_name} "
            f"{obj.member.last_name}"
        ).strip()

    def get_membership_name(self, obj):

        if not obj.membership:
            return None

        return obj.membership.plan.name

    def get_organization_name(self, obj):

        if not obj.organization:
            return None

        return obj.organization.name

    def get_branch_name(self, obj):

        if not obj.branch:
            return None

        return obj.branch.name

    def get_collected_by_name(self, obj):

        if not obj.collected_by:
            return None

        return (
            f"{obj.collected_by.first_name} "
            f"{obj.collected_by.last_name}"
        ).strip()

    def validate_amount(self, value):

        if value <= Decimal("0"):
            raise serializers.ValidationError(
                "Payment amount must be greater than zero."
            )

        return value

    def validate_discount(self, value):

        if value < Decimal("0"):
            raise serializers.ValidationError(
                "Discount cannot be negative."
            )

        return value

    def validate_tax(self, value):

        if value < Decimal("0"):
            raise serializers.ValidationError(
                "Tax cannot be negative."
            )

        return value

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

        membership = attrs.get(
            "membership",
            getattr(
                self.instance,
                "membership",
                None,
            )
            if self.instance
            else None,
        )

        amount = attrs.get(
            "amount",
            getattr(
                self.instance,
                "amount",
                Decimal("0"),
            )
            if self.instance
            else Decimal("0"),
        )

        discount = attrs.get(
            "discount",
            getattr(
                self.instance,
                "discount",
                Decimal("0"),
            )
            if self.instance
            else Decimal("0"),
        )

        if discount > amount:
            raise serializers.ValidationError(
                {
                    "discount": (
                        "Discount cannot be greater than "
                        "the payment amount."
                    )
                }
            )

        if membership and member:

            if membership.member_id != member.id:
                raise serializers.ValidationError(
                    {
                        "membership": (
                            "Selected membership does not "
                            "belong to the selected member."
                        )
                    }
                )

        return attrs