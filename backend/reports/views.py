from rest_framework.views import APIView
from roles.permissions import RolePermission
from rest_framework.response import Response

from .services import ReportsService


class BusinessReportView(APIView):

    permission_classes = [RolePermission]
    required_permission = "reports.view"

    def get(self, request):

        data = ReportsService.get_business_report()

        return Response(data)