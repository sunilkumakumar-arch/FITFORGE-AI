from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import BootstrapSerializer
from .super_admin_service import BootstrapSuperAdminService
from rest_framework.permissions import AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication


class BootstrapInstallAPIView(APIView):
    """
    Performs the first-time FitForge installation.
    """
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = BootstrapSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = BootstrapSuperAdminService.run(
            serializer.validated_data
        )

        return Response(
            {
                "success": True,
                "message": "FitForge installed successfully.",
                "data": {
                    "employee_code": result["employee_code"],
                    "temporary_password": result["temporary_password"],
                },
            },
            status=status.HTTP_201_CREATED,
        )