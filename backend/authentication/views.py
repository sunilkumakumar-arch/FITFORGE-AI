from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.throttling import ScopedRateThrottle

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)

from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
)

from .serializers import LoginSerializer
from .change_password_serializer import ChangePasswordSerializer
from .logout_serializer import LogoutSerializer
from .services import AuthenticationService


# ==========================================================
# RESPONSE SCHEMAS
# ==========================================================


class TokenResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()


class UserSessionUserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    full_name = serializers.CharField()
    email = serializers.EmailField(allow_blank=True)


class UserSessionEmployeeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    employee_code = serializers.CharField()
    employment_type = serializers.CharField()
    employee_classification = serializers.CharField()
    employment_status = serializers.CharField()


class UserSessionOrganizationSerializer(serializers.Serializer):
    id = serializers.IntegerField(allow_null=True)
    name = serializers.CharField(
        allow_null=True,
        allow_blank=True,
    )


class UserSessionBranchSerializer(serializers.Serializer):
    id = serializers.IntegerField(allow_null=True)
    name = serializers.CharField(
        allow_null=True,
        allow_blank=True,
    )


class UserSessionDepartmentSerializer(serializers.Serializer):
    id = serializers.IntegerField(allow_null=True)
    name = serializers.CharField(
        allow_null=True,
        allow_blank=True,
    )


class UserSessionDesignationSerializer(serializers.Serializer):
    id = serializers.IntegerField(allow_null=True)
    name = serializers.CharField(
        allow_null=True,
        allow_blank=True,
    )


class UserSessionRoleSerializer(serializers.Serializer):
    id = serializers.IntegerField(allow_null=True)
    code = serializers.CharField(
        allow_null=True,
        allow_blank=True,
    )
    name = serializers.CharField(
        allow_null=True,
        allow_blank=True,
    )


class UserSessionProfileSerializer(serializers.Serializer):
    must_change_password = serializers.BooleanField()
    account_locked = serializers.BooleanField()
    language = serializers.CharField()
    timezone = serializers.CharField()
    profile_photo = serializers.URLField(
        allow_null=True,
    )


class UserSessionSerializer(serializers.Serializer):
    user = UserSessionUserSerializer()
    employee = UserSessionEmployeeSerializer()
    organization = UserSessionOrganizationSerializer()
    branch = UserSessionBranchSerializer()
    department = UserSessionDepartmentSerializer()
    designation = UserSessionDesignationSerializer()
    role = UserSessionRoleSerializer()
    profile = UserSessionProfileSerializer()


class LoginResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    tokens = TokenResponseSerializer()
    session = UserSessionSerializer()


class MessageResponseSerializer(serializers.Serializer):
    message = serializers.CharField()


# ==========================================================
# LOGIN
# ==========================================================


class LoginView(APIView):
    """
    Enterprise Login API.
    """

    authentication_classes = []
    permission_classes = [AllowAny]

    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "login"

    @extend_schema(
        request=LoginSerializer,
        responses={
            200: LoginResponseSerializer,
            400: OpenApiResponse(
                description="Invalid login request."
            ),
            401: OpenApiResponse(
                description="Invalid employee code or password."
            ),
        },
        tags=["Authentication"],
        operation_id="authentication_login",
    )
    def post(self, request):

        serializer = LoginSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        result = AuthenticationService.login(
            request=request,
            employee_code=serializer.validated_data[
                "employee_code"
            ],
            password=serializer.validated_data[
                "password"
            ],
        )

        return Response(
            result,
            status=status.HTTP_200_OK,
        )


# ==========================================================
# CHANGE PASSWORD
# ==========================================================


class ChangePasswordView(APIView):
    """
    Change Password API.
    """

    permission_classes = [IsAuthenticated]

    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "change_password"

    @extend_schema(
        request=ChangePasswordSerializer,
        responses={
            200: MessageResponseSerializer,
            400: OpenApiResponse(
                description="Invalid password request."
            ),
            401: OpenApiResponse(
                description="Authentication failed."
            ),
        },
        tags=["Authentication"],
        operation_id="authentication_change_password",
    )
    def post(self, request):

        serializer = ChangePasswordSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        result = AuthenticationService.change_password(
            user=request.user,
            current_password=serializer.validated_data[
                "current_password"
            ],
            new_password=serializer.validated_data[
                "new_password"
            ],
        )

        return Response(
            result,
            status=status.HTTP_200_OK,
        )


# ==========================================================
# CURRENT USER
# ==========================================================


class CurrentUserView(APIView):
    """
    Return the authenticated user's session.
    """

    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={
            200: UserSessionSerializer,
            401: OpenApiResponse(
                description="Authentication required."
            ),
        },
        tags=["Authentication"],
        operation_id="authentication_current_user",
    )
    def get(self, request):

        session = AuthenticationService.get_current_user(
            request.user
        )

        return Response(
            session,
            status=status.HTTP_200_OK,
        )


# ==========================================================
# LOGOUT
# ==========================================================


class LogoutView(APIView):
    """
    Logout API.
    """

    permission_classes = [IsAuthenticated]

    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "logout"

    @extend_schema(
        request=LogoutSerializer,
        responses={
            200: MessageResponseSerializer,
            400: OpenApiResponse(
                description="Invalid logout request."
            ),
            401: OpenApiResponse(
                description="Authentication failed."
            ),
        },
        tags=["Authentication"],
        operation_id="authentication_logout",
    )
    def post(self, request):

        serializer = LogoutSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        result = AuthenticationService.logout(
            refresh_token=serializer.validated_data[
                "refresh"
            ],
        )

        return Response(
            result,
            status=status.HTTP_200_OK,
        )