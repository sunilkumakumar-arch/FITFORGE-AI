from rest_framework import serializers


class QRScanSerializer(serializers.Serializer):
    """
    Serializer for QR attendance scanning.
    """

    qr_payload = serializers.CharField()

    branch_id = serializers.IntegerField()

    device_id = serializers.CharField(
        required=False,
        allow_blank=True,
        default="",
    )