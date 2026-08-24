from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

from .models import MemberHub


class MemberHubSerializer(serializers.ModelSerializer):
    """
    Serializer for the MemberHub module.
    """

    qr_code = serializers.SerializerMethodField()

    member_code = serializers.CharField(
        source="member.member_code",
        read_only=True,
    )

    first_name = serializers.CharField(
        source="member.first_name",
        read_only=True,
    )

    last_name = serializers.CharField(
        source="member.last_name",
        read_only=True,
    )

    phone = serializers.CharField(
        source="member.phone",
        read_only=True,
    )

    email = serializers.EmailField(
        source="member.email",
        read_only=True,
    )

    class Meta:
        model = MemberHub

        fields = (
            "member_code",
            "public_member_id",
            "first_name",
            "last_name",
            "phone",
            "email",
            "card_level",
            "card_version",
            "qr_code",
        )

        read_only_fields = fields

    @extend_schema_field(
        serializers.URLField(allow_null=True)
    )
    def get_qr_code(self, obj):
        request = self.context.get("request")

        if not obj.qr_code:
            return None

        if request:
            return request.build_absolute_uri(
                obj.qr_code.url
            )

        return obj.qr_code.url