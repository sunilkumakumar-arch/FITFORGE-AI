from rest_framework import serializers

from accounts.models import Member
from .models import MembershipPlan


class PurchaseMembershipSerializer(serializers.Serializer):

    member_id = serializers.PrimaryKeyRelatedField(
        queryset=Member.objects.all(),
        source="member",
    )

    plan_id = serializers.PrimaryKeyRelatedField(
        queryset=MembershipPlan.objects.filter(is_active=True),
        source="plan",
    )

    amount_paid = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    payment_method = serializers.CharField()

    transaction_id = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    notes = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    start_date = serializers.DateField(
        required=False,
    )