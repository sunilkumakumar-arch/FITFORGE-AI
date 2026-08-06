from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.throttling import ScopedRateThrottle

from .serializers import LoginSerializer
from .services import AuthenticationService

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)

from .change_password_serializer import ChangePasswordSerializer

from .logout_serializer import LogoutSerializer


class LoginView(APIView):
    """
    Enterprise Login API
    """

    authentication_classes = []
    permission_classes = [AllowAny]
    
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "login"        

    def post(self, request):



        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = AuthenticationService.login(
            request=request,
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

    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "change_password"

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


class CurrentUserView(APIView):
    """
    Return the authenticated user's session.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):

        session = AuthenticationService.get_current_user(
            request.user
        )

        return Response(
            session,
            status=status.HTTP_200_OK,
        )    

class LogoutView(APIView):
    """
    Logout API
    """

    permission_classes = [IsAuthenticated]
    
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "logout"

    def post(self, request):

        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = AuthenticationService.logout(
            refresh_token=serializer.validated_data["refresh"],
        )

        return Response(
            result,
            status=status.HTTP_200_OK,
        )    