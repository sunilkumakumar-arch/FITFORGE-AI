from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import LoginSerializer
from .services import AuthenticationService

from rest_framework.permissions import IsAuthenticated

from .change_password_serializer import ChangePasswordSerializer


class LoginView(APIView):
    """
    Enterprise Login API
    """

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = AuthenticationService.login(
            employee_code=serializer.validated_data["employee_code"],
            password=serializer.validated_data["password"],
        )

        return Response(
            result,
            status=status.HTTP_200_OK,
        )

class ChangePasswordView(APIView):
    """
    Change Password API
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = AuthenticationService.change_password(
            user=request.user,
            current_password=serializer.validated_data["current_password"],
            new_password=serializer.validated_data["new_password"],
        )

        return Response(
            result,
            status=status.HTTP_200_OK,
        )    