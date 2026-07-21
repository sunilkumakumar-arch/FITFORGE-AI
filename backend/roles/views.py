from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from roles.models import Role
from roles.serializers import (
    RoleSerializer,
    PermissionSerializer,
    AssignPermissionSerializer,
)
from roles.services import RoleService


class RoleListCreateAPIView(APIView):

    def get(self, request):

        roles = RoleService.get_roles()

        serializer = RoleSerializer(
            roles,
            many=True,
        )

        return Response(serializer.data)

    def post(self, request):

        serializer = RoleSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        role = RoleService.create_role(
            serializer.validated_data
        )

        return Response(
            RoleSerializer(role).data,
            status=status.HTTP_201_CREATED,
        )


class PermissionListAPIView(APIView):

    def get(self, request):

        permissions = RoleService.get_permissions()

        serializer = PermissionSerializer(
            permissions,
            many=True,
        )

        return Response(serializer.data)


class AssignPermissionAPIView(APIView):

    def post(
        self,
        request,
        role_id,
    ):

        serializer = AssignPermissionSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        role = RoleService.assign_permissions(
            role_id=role_id,
            permission_ids=serializer.validated_data[
                "permission_ids"
            ],
        )

        return Response(
            RoleSerializer(role).data
        )