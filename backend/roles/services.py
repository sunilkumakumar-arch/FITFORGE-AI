from django.shortcuts import get_object_or_404

from roles.models import Role, Permission


class RoleService:

    @staticmethod
    def get_roles():
        return Role.objects.prefetch_related(
            "permissions"
        ).all()

    @staticmethod
    def get_permissions():
        return Permission.objects.all().order_by(
            "module",
            "name",
        )

    @staticmethod
    def assign_permissions(
        role_id,
        permission_ids,
    ):
        role = get_object_or_404(
            Role,
            id=role_id,
        )

        permissions = Permission.objects.filter(
            id__in=permission_ids
        )

        role.permissions.set(permissions)

        return role

    @staticmethod
    def create_role(
        validated_data,
    ):
        return Role.objects.create(
            **validated_data
        )