from rest_framework import serializers

from .models import (
    PTPackage,
    MemberPTPackage,
    PTSession
)


class PTPackageSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = PTPackage
        fields = "__all__"


class MemberPTPackageSerializer(
    serializers.ModelSerializer
):

    member_name = serializers.CharField(
        source="member.first_name",
        read_only=True
    )

    package_name = serializers.CharField(
        source="package.name",
        read_only=True
    )

    sessions_remaining = serializers.ReadOnlyField()

    class Meta:
        model = MemberPTPackage
        fields = "__all__"


class PTSessionSerializer(
    serializers.ModelSerializer
):

    member_name = serializers.CharField(
        source=(
            "member_package.member.first_name"
        ),
        read_only=True
    )

    trainer_name = serializers.CharField(
        source="trainer.first_name",
        read_only=True
    )

    class Meta:
        model = PTSession
        fields = "__all__"