
from django.utils import timezone

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Attendance
from .serializers import AttendanceSerializer
from .services import AttendanceService

from accounts.models import Member


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
    
