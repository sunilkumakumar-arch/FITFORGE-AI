from rest_framework.views import APIView
from roles.permissions import RolePermission
from rest_framework.response import Response

from .services import DashboardService


class DashboardSummaryView(APIView):

    permission_classes = [RolePermission]
    permission_map = {
        "list": "dashboard.view",
        "summary": "dashboard.view",
    }

    def get(self, request):

        data = DashboardService.get_summary()

        return Response(data)