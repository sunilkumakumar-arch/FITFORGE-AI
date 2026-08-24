from rest_framework import serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
)

from .serializers import BootstrapSerializer
from .super_admin_service import BootstrapSuperAdminService


# ==========================================================
# RESPONSE SCHEMAS
# ==========================================================


class BootstrapDataSerializer(serializers.Serializer):
    employee_code = serializers.CharField()
    temporary_password = serializers.CharField()


class BootstrapResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    message = serializers.CharField()
    data = BootstrapDataSerializer()


# ==========================================================
# BOOTSTRAP INSTALLATION
# ==========================================================


class BootstrapInstallAPIView(APIView):
    """
    Performs the first-time FitForge installation.
    """

    authentication_classes = []
    permission_classes = [AllowAny]

    @extend_schema(
        request=BootstrapSerializer,
        responses={
            201: BootstrapResponseSerializer,
            400: OpenApiResponse(
                description="Invalid installation data."
            ),
        },
        tags=["Authentication"],
        operation_id="bootstrap_install",
    )
    def post(self, request):

        serializer = BootstrapSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        result = BootstrapSuperAdminService.run(
            serializer.validated_data
        )

        return Response(
            {
                "success": True,
                "message": "FitForge installed successfully.",
                "data": {
                    "employee_code": result["employee_code"],
                    "temporary_password": result[
                        "temporary_password"
                    ],
                },
            },
            status=status.HTTP_201_CREATED,
        )