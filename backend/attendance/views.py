from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from roles.permissions import RolePermission

from core.models import Branch
from accounts.models import Member

from member_hub.verification_service import VerificationService

from .models import Attendance
from .serializers import AttendanceSerializer
from .qr_serializers import QRScanSerializer
from .services import AttendanceService


class AttendanceViewSet(viewsets.ModelViewSet):
    """
    Enterprise Attendance Management API.
    """

    queryset = (
        Attendance.objects
        .select_related(
            "member",
            "trainer",
            "branch",
            "branch__organization",
        )
        .order_by(
            "-attendance_date",
            "-id",
        )
    )

    serializer_class = AttendanceSerializer

    permission_classes = [
        RolePermission,
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

    def get_queryset(self):
        """
        Apply organization / branch tenant isolation.
        """

        queryset = super().get_queryset()

        user = self.request.user

        if not user.is_authenticated:
            return queryset.none()

        if user.is_superuser:
            return queryset

        try:
            employee = user.employee_profile
        except Exception:
            return queryset.none()

        if not employee.role:
            return queryset.none()

        role_code = employee.role.code

        if role_code == "SUPER_ADMIN":
            return queryset

        if role_code == "ORG_OWNER":

            if not employee.organization_id:
                return queryset.none()

            return queryset.filter(
                branch__organization_id=employee.organization_id
            )

        if role_code == "BRANCH_MANAGER":

            if not employee.branch_id:
                return queryset.none()

            return queryset.filter(
                branch_id=employee.branch_id
            )

        return queryset.none()

    @action(
        detail=False,
        methods=["get"],
    )
    def today_count(self, request):

        today = timezone.now().date()

        count = self.get_queryset().filter(
            attendance_date=today
        ).count()

        return Response({
            "today_attendance": count,
        })

    @action(
        detail=False,
        methods=["get"],
    )
    def today_members(self, request):

        today = timezone.now().date()

        records = (
            self.get_queryset()
            .filter(
                attendance_date=today
            )
            .order_by("-check_in")
        )

        serializer = self.get_serializer(
            records,
            many=True,
        )

        return Response(serializer.data)

    @action(
        detail=False,
        methods=["post"],
        url_path="check-in",
    )
    def check_in(self, request):

        member_id = request.data.get("member")
        branch_id = request.data.get("branch")

        if not member_id:
            return Response(
                {
                    "success": False,
                    "message": "Member ID is required.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not branch_id:
            return Response(
                {
                    "success": False,
                    "message": "Branch ID is required.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        member = get_object_or_404(
            Member,
            id=member_id,
        )

        branch = get_object_or_404(
            Branch,
            id=branch_id,
        )

        # Ensure the logged-in employee can operate
        # on this branch.
        allowed_branch_queryset = (
            self.get_queryset()
            .filter(branch=branch)
        )

        if not request.user.is_superuser:

            employee = getattr(
                request.user,
                "employee_profile",
                None,
            )

            if not employee:
                return Response(
                    {
                        "success": False,
                        "message": "Employee profile not found.",
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

            role_code = (
                employee.role.code
                if employee.role
                else None
            )

            if role_code == "ORG_OWNER":

                if (
                    employee.organization_id
                    != branch.organization_id
                ):
                    return Response(
                        {
                            "success": False,
                            "message": "You do not have access to this branch.",
                        },
                        status=status.HTTP_403_FORBIDDEN,
                    )

            elif role_code == "BRANCH_MANAGER":

                if employee.branch_id != branch.id:
                    return Response(
                        {
                            "success": False,
                            "message": "You do not have access to this branch.",
                        },
                        status=status.HTTP_403_FORBIDDEN,
                    )

            elif role_code != "SUPER_ADMIN":

                return Response(
                    {
                        "success": False,
                        "message": "You do not have permission to mark attendance.",
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

        result = AttendanceService.check_in(
            member=member,
            branch=branch,
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

    @action(
        detail=False,
        methods=["post"],
        url_path="check-out",
    )
    def check_out(self, request):

        member_id = request.data.get("member")

        if not member_id:
            return Response(
                {
                    "success": False,
                    "message": "Member ID is required.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        member = get_object_or_404(
            Member,
            id=member_id,
        )

        attendance = (
            AttendanceService
            .get_today_attendance(member)
        )

        if not attendance:
            return Response(
                {
                    "success": False,
                    "message": "No check-in found for today.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check whether the logged-in employee can
        # access the attendance branch.
        if not self.get_queryset().filter(
            id=attendance.id
        ).exists():
            return Response(
                {
                    "success": False,
                    "message": "You do not have access to this attendance record.",
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        result = AttendanceService.check_out(member)

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

    @action(
        detail=False,
        methods=["post"],
        url_path="scan",
    )
    def scan(self, request):
        """
        QR Attendance Scanner.
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

        # Validate that the logged-in employee can
        # operate on this branch.
        if not request.user.is_superuser:

            employee = getattr(
                request.user,
                "employee_profile",
                None,
            )

            if not employee:
                return Response(
                    {
                        "success": False,
                        "message": "Employee profile not found.",
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

            role_code = (
                employee.role.code
                if employee.role
                else None
            )

            if role_code == "ORG_OWNER":

                if (
                    employee.organization_id
                    != branch.organization_id
                ):
                    return Response(
                        {
                            "success": False,
                            "message": "You do not have access to this branch.",
                        },
                        status=status.HTTP_403_FORBIDDEN,
                    )

            elif role_code == "BRANCH_MANAGER":

                if employee.branch_id != branch.id:
                    return Response(
                        {
                            "success": False,
                            "message": "You do not have access to this branch.",
                        },
                        status=status.HTTP_403_FORBIDDEN,
                    )

            elif role_code != "SUPER_ADMIN":

                return Response(
                    {
                        "success": False,
                        "message": "You do not have permission to mark attendance.",
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

        result = AttendanceService.scan_qr(
            member=member,
            branch=branch,
            device_id=serializer.validated_data[
                "device_id"
            ],
        )

        if result.get("attendance"):
            result["attendance"] = AttendanceSerializer(
                result["attendance"]
            ).data

        return Response(
            result,
            status=(
                status.HTTP_200_OK
                if result["success"]
                else status.HTTP_400_BAD_REQUEST
            ),
        )