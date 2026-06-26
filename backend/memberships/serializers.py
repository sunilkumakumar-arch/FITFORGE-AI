from rest_framework import serializers
from .models import MembershipPlan, MemberMembership


class MembershipPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipPlan
        fields = "__all__"


class MemberMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberMembership
        fields = "__all__"