from rest_framework import serializers

from roles.models import Role, Permission


class PermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permission

        fields = [
            "id",
            "module",
            "code",
            "name",
            "description",
        ]


class RoleSerializer(serializers.ModelSerializer):

    permissions = PermissionSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Role

        fields = [
            "id",
            "name",
            "description",
            "is_system_role",
            "is_active",
            "permissions",
        ]

class AssignPermissionSerializer(serializers.Serializer):

    permission_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False,
    )