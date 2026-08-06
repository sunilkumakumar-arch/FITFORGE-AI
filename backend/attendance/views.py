from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework import status, viewsets
from rest_framework.decorators import action
from roles.permissions import RolePermission
from rest_framework.response import Response

from core.models import Branch
from accounts.models import Member

from member_hub.verification_service import VerificationService

from .models import Attendance
from .serializers import AttendanceSerializer
from .qr_serializers import QRScanSerializer
from .services import AttendanceService


class AttendanceViewSet(viewsets.ModelViewSet):

    queryset = (
        Attendance.objects
        .select_related(
            "member",
            "trainer",
            "branch",
        )
        .order_by("-attendance_date", "-id")
    )

    serializer_class = AttendanceSerializer

    permission_classes = [
        RolePermission
    ]

    permission_map = {
        "list": "attendance.view",
        "retrieve": "attendance.view",
        "today_count": "attendance.view",
        "today_members": "attendance.view",
        "create": "attendance.mark",
        "check_in": "attendance.mark",
        "check_out": "attendance.mark",
        "scan": "attendance.mark",
        "update": "attendance.update",
        "partial_update": "attendance.update",
        "destroy": "attendance.delete",
    }

    @action(
        detail=False,
        methods=["get"]
    )
    def today_count(self, request):

        today = timezone.now().date()

        count = Attendance.objects.filter(
            attendance_date=today
        ).count()

        return Response({
            "today_attendance": count
        })

    @action(
        detail=False,
        methods=["get"]
    )
    def today_members(self, request):

        today = timezone.now().date()

        records = (
            Attendance.objects
            .select_related(
                "member",
                "trainer",
                "branch",
            )
            .filter(
                attendance_date=today
            )
            .order_by("-check_in")
        )

        serializer = self.get_serializer(
            records,
            many=True
        )

        return Response(serializer.data)

    @action(
        detail=False,
        methods=["post"],
        url_path="check-in"
    )
    def check_in(self, request):

        member_id = request.data.get("member")

        if not member_id:
            return Response(
                {
                    "success": False,
                    "message": "Member ID is required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        member = get_object_or_404(
            Member,
            id=member_id,
        )

        result = AttendanceService.check_in(
            member=member,
            branch=member.branch,
            trainer=None,
            checkin_method=request.data.get(
                "checkin_method",
                "Reception"
            ),
            device_id=request.data.get(
                "device_id",
                ""
            )
        )

        return Response(
            result,
            status=status.HTTP_200_OK
            if result["success"]
            else status.HTTP_400_BAD_REQUEST
        )

    @action(
        detail=False,
        methods=["post"],
        url_path="check-out"
    )
    def check_out(self, request):

        member_id = request.data.get("member")

        if not member_id:
            return Response(
                {
                    "success": False,
                    "message": "Member ID is required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        member = get_object_or_404(
            Member,
            id=member_id,
        )

        result = AttendanceService.check_out(member)

        return Response(
            result,
            status=status.HTTP_200_OK
            if result["success"]
            else status.HTTP_400_BAD_REQUEST
        )

    @action(
        detail=False,
        methods=["post"],
        url_path="scan"
    )
    def scan(self, request):
        """
        QR Attendance Scanner
        """

        serializer = QRScanSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        verification = VerificationService.verify_qr(
            serializer.validated_data["qr_payload"]
        )

        if not verification["valid"]:
            return Response(
                verification,
                status=status.HTTP_400_BAD_REQUEST,
            )

        member = verification["member_hub"].member

        branch = get_object_or_404(
            Branch,
            id=serializer.validated_data["branch_id"],
        )

        result = AttendanceService.scan_qr(
            member=member,
            branch=branch,
            device_id=serializer.validated_data["device_id"],
        )

        if result.get("attendance"):
            result["attendance"] = AttendanceSerializer(
                result["attendance"]
            ).data

        return Response(
            result,
            status=status.HTTP_200_OK
            if result["success"]
            else status.HTTP_400_BAD_REQUEST
        )