from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema

from roles.permissions import RolePermission

from .selectors import MemberHubSelector
from .serializers import MemberHubSerializer
from .verification_serializers import QRVerificationSerializer
from .verification_service import VerificationService


class MemberHubListView(generics.ListAPIView):
    """
    Returns all MemberHub records.
    """

    serializer_class = MemberHubSerializer
    permission_classes = [RolePermission]

    required_permission = "member.view"

    def get_queryset(self):
        return MemberHubSelector.get_queryset()


class MemberHubDetailView(generics.RetrieveAPIView):
    """
    Returns a single MemberHub by primary key.
    """

    serializer_class = MemberHubSerializer
    permission_classes = [RolePermission]

    required_permission = "member.view"

    def get_queryset(self):
        return MemberHubSelector.get_queryset()


class MemberHubByPublicIdView(generics.RetrieveAPIView):
    """
    Returns a MemberHub by public_member_id.
    """

    serializer_class = MemberHubSerializer
    permission_classes = [RolePermission]

    required_permission = "member.view"

    def get_object(self):
        return MemberHubSelector.get_by_public_member_id(
            self.kwargs["public_member_id"]
        )


class MemberHubByMemberCodeView(generics.RetrieveAPIView):
    """
    Returns a MemberHub by member_code.
    """

    serializer_class = MemberHubSerializer
    permission_classes = [RolePermission]

    required_permission = "member.view"

    def get_object(self):
        return MemberHubSelector.get_by_member_code(
            self.kwargs["member_code"]
        )


class QRVerificationView(APIView):
    """
    Verifies a scanned member QR code.
    """

    @extend_schema(
        request=QRVerificationSerializer,
        responses={
            200: MemberHubSerializer,
        },
        tags=["Member Hub"],
    )
    def post(self, request):

        serializer = QRVerificationSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        result = VerificationService.verify_qr(
            serializer.validated_data["qr_payload"]
        )

        if not result["valid"]:
            return Response(
                result,
                status=status.HTTP_400_BAD_REQUEST,
            )

        member_serializer = MemberHubSerializer(
            result["member_hub"],
            context={
                "request": request,
            },
        )

        return Response(
            {
                "valid": True,
                "member": member_serializer.data,
            },
            status=status.HTTP_200_OK,
        )