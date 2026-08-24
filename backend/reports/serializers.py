from rest_framework import serializers


class BusinessReportSerializer(serializers.Serializer):
    """
    Serializer for the business report response.
    """

    total_members = serializers.IntegerField()
    active_memberships = serializers.IntegerField()
    expired_memberships = serializers.IntegerField()
    total_trainers = serializers.IntegerField()
    today_attendance = serializers.IntegerField()
    total_revenue = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
    )
    total_payments = serializers.IntegerField()
    pending_payments = serializers.IntegerField()