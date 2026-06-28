from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .services import ReportsService


class BusinessReportView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        data = ReportsService.get_business_report()

        return Response(data)