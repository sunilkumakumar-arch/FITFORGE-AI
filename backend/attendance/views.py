from django.utils import timezone

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import Branch
from accounts.models import Member

from member_hub.verification_service import VerificationService

from .models import Attendance
from .serializers import AttendanceSerializer
from .qr_serializers import QRScanSerializer
from .services import AttendanceService


class AttendanceViewSet(
    viewsets.ModelViewSet
):

    queryset = Attendance.objects.select_related(
        "member",
        "trainer",
        "branch"
    )

    serializer_class = AttendanceSerializer

    permission_classes = [
        IsAuthenticated
    ]

    @action(
        detail=False,
        methods=["get"]
    )
    def today_count(
        self,
        request
    ):
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
    def today_members(
        self,
        request
    ):
        today = timezone.now().date()

        records = Attendance.objects.filter(
            attendance_date=today
        )

        serializer = self.get_serializer(
            records,
            many=True
        )

        return Response(
            serializer.data
        )
    

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
                status=400
            )

        try:
            member = Member.objects.get(id=member_id)
        except Member.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": "Member not found."
                },
                status=404
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
            status=200 if result["success"] else 400
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
                status=400
            )

        try:
            member = Member.objects.get(id=member_id)
        except Member.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": "Member not found."
                },
                status=404
            )

        result = AttendanceService.check_out(member)

        return Response(
            result,
            status=200 if result["success"] else 400
        )

    @action(detail=False, methods=["post"], url_path="scan")
    def scan(self, request):
        """
        QR Attendance Scanner
        """

        serializer = QRScanSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        verification = VerificationService.verify_qr(
            serializer.validated_data["qr_payload"]
        )

        if not verification["valid"]:
            return Response(
                verification,
                status=status.HTTP_400_BAD_REQUEST,
            )

        member = verification["member_hub"].member

        try:
            branch = Branch.objects.get(
                id=serializer.validated_data["branch_id"]
            )
        except Branch.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": "Branch not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        result = AttendanceService.scan_qr(
            member=member,
            branch=branch,
            device_id=serializer.validated_data["device_id"],
        )

        # Convert Attendance model to JSON
        if result.get("attendance"):
            attendance_serializer = AttendanceSerializer(
                result["attendance"]
            )
            result["attendance"] = attendance_serializer.data

        return Response(
            result,
            status=200 if result["success"] else 400
        )

