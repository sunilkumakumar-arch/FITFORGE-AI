from rest_framework.views import APIView
from roles.permissions import RolePermission
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from .services import ReportsService
from .serializers import BusinessReportSerializer


class BusinessReportView(APIView):
    """
    Returns the business report.
    """

    permission_classes = [RolePermission]
    required_permission = "reports.view"

    @extend_schema(
        responses=BusinessReportSerializer,
    )
    def get(self, request):

        data = ReportsService.get_business_report()

        serializer = BusinessReportSerializer(data)

        return Response(serializer.data)