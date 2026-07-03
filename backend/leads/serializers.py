# leads/serializers.py

from rest_framework import serializers

from .models import (
    Lead,
    LeadFollowUp
)


class LeadSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = Lead
        fields = "__all__"


class LeadFollowUpSerializer(
    serializers.ModelSerializer
):

    lead_name = serializers.CharField(
        source="lead.first_name",
        read_only=True
    )

    class Meta:
        model = LeadFollowUp
        fields = "__all__"