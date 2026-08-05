from rest_framework import serializers


class QRVerificationSerializer(serializers.Serializer):
    """
    Serializer for QR verification requests.
    """

    qr_payload = serializers.CharField()