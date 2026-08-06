from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework import status
from roles.permissions import RolePermission
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Member
from memberships.models import MembershipPlan
from memberships.services import MembershipPurchaseService

from .serializers import (
    ReceptionDashboardSerializer,
    MembershipRenewSerializer,
)
from .services import ReceptionDashboardService


class ReceptionMemberDashboardAPIView(APIView):
    permission_classes = [RolePermission]
    required_permission = "member.view"

    def get(self, request, member_code):

        result = ReceptionDashboardService.get_member_dashboard(member_code)

        if not result["success"]:
            return Response(
                result,
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = ReceptionDashboardSerializer(result)

        return Response(serializer.data)


class ReceptionSearchAPIView(APIView):
    permission_classes = [RolePermission]
    required_permission = "member.view"

    def get(self, request):

        query = request.GET.get("q", "").strip()

        if not query:
            return Response(
                {
                    "success": False,
                    "message": "Search query is required.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        result = ReceptionDashboardService.search_members(query)

        return Response(result)


class ReceptionRenewAPIView(APIView):
    permission_classes = [RolePermission]
    required_permission = "member.view"

    def post(self, request, member_code):

        serializer = MembershipRenewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        member = get_object_or_404(
            Member,
            member_code=member_code,
        )

        plan = get_object_or_404(
            MembershipPlan,
            id=data["membership_plan_id"],
            is_active=True,
        )

        try:
            membership = MembershipPurchaseService.purchase_membership(
                member=member,
                plan=plan,
                start_date=timezone.now().date(),
                amount_paid=data["amount_paid"],
                payment_method=data["payment_method"],
                transaction_id=data.get("transaction_id", ""),
                notes="Reception Membership Renewal",
            )

            return Response(
                {
                    "success": True,
                    "message": "Membership renewed successfully.",
                    "membership_id": membership.id,
                    "status": membership.status,
                    "start_date": membership.start_date.isoformat(),
                    "end_date": membership.end_date.isoformat(),
                },
                status=status.HTTP_201_CREATED,
            )

        except ValueError as e:
            return Response(
                {
                    "success": False,
                    "message": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": "An unexpected error occurred while processing the renewal.",
                    "error": str(e),  # Remove this line in production if you don't want to expose errors
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )