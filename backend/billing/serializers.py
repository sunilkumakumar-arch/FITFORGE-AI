from rest_framework import serializers

from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):

    member_name = serializers.SerializerMethodField()

    membership_plan_name = serializers.SerializerMethodField()

    class Meta:
        model = Payment

        fields = [
            "id",
            "member",
            "member_name",
            "membership_plan",
            "membership_plan_name",
            "amount",
            "payment_method",
            "payment_status",
            "payment_date",
            "transaction_id",
            "notes",
            "created_at",
            "updated_at",
        ]

    def get_member_name(self, obj):
        return (
            f"{obj.member.first_name} "
            f"{obj.member.last_name}"
        )

    def get_membership_plan_name(self, obj):
        if obj.membership_plan:
            return obj.membership_plan.name

        return None