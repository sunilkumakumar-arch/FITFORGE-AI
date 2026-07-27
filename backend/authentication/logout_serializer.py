from rest_framework import serializers


class LogoutSerializer(serializers.Serializer):
    """
    Logout Serializer
    """

    refresh = serializers.CharField()