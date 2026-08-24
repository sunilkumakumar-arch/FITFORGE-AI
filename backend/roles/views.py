from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from roles.models import Role
from roles.serializers import (
    RoleSerializer,
    PermissionSerializer,
    AssignPermissionSerializer,
)
from roles.services import RoleService


class RoleListCreateAPIView(APIView):

    @extend_schema(
        responses=RoleSerializer(many=True),
    )
    def get(self, request):

        roles = RoleService.get_roles()

        serializer = RoleSerializer(
            roles,
            many=True,
        )

        return Response(serializer.data)

    @extend_schema(
        request=RoleSerializer,
        responses={
            201: RoleSerializer,
        },
    )
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

    @extend_schema(
        responses=PermissionSerializer(many=True),
    )
    def get(self, request):

        permissions = RoleService.get_permissions()

        serializer = PermissionSerializer(
            permissions,
            many=True,
        )

        return Response(serializer.data)


class AssignPermissionAPIView(APIView):

    @extend_schema(
        request=AssignPermissionSerializer,
        responses=RoleSerializer,
    )
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