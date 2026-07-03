from django.db.models import Count
from django.utils import timezone

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Attendance
from .serializers import AttendanceSerializer


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