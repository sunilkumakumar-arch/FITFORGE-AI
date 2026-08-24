from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
)

from roles.permissions import RolePermission

from .services import DashboardService


# ==========================================================
# RESPONSE SCHEMA
# ==========================================================


class DashboardSummarySerializer(serializers.Serializer):
    total_members = serializers.IntegerField()
    total_employees = serializers.IntegerField()
    total_trainers = serializers.IntegerField()
    active_memberships = serializers.IntegerField()
    expired_memberships = serializers.IntegerField()
    today_attendance = serializers.IntegerField()
    total_revenue = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
    )
    total_payments = serializers.IntegerField()
    pending_payments = serializers.IntegerField()


# ==========================================================
# DASHBOARD SUMMARY
# ==========================================================


class DashboardSummaryView(APIView):

    permission_classes = [RolePermission]

    permission_map = {
        "list": "dashboard.view",
        "summary": "dashboard.view",
    }

    @extend_schema(
        responses={
            200: DashboardSummarySerializer,
            403: OpenApiResponse(
                description="Permission denied."
            ),
        },
        tags=["Dashboard"],
        operation_id="dashboard_summary",
    )
    def get(self, request):

        data = DashboardService.get_summary()

        return Response(data)