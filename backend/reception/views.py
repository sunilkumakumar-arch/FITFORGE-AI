from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema

from accounts.models import Member
from memberships.models import MembershipPlan
from memberships.services import MembershipPurchaseService
from roles.permissions import RolePermission

from .serializers import (
    ReceptionDashboardSerializer,
    MembershipRenewSerializer,
)
from .services import ReceptionDashboardService


# ==========================================================
# RESPONSE SERIALIZERS
# ==========================================================


class ReceptionSearchResultSerializer(
    serializers.Serializer
):
    member_code = serializers.CharField()
    name = serializers.CharField()
    phone = serializers.CharField()
    membership_status = serializers.CharField()


class ReceptionSearchResponseSerializer(
    serializers.Serializer
):
    success = serializers.BooleanField()
    count = serializers.IntegerField()
    results = ReceptionSearchResultSerializer(
        many=True
    )


class ReceptionRenewResponseSerializer(
    serializers.Serializer
):
    success = serializers.BooleanField()
    message = serializers.CharField()
    membership_id = serializers.IntegerField()
    status = serializers.CharField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()


# ==========================================================
# MEMBER DASHBOARD
# ==========================================================


class ReceptionMemberDashboardAPIView(
    APIView
):

    permission_classes = [RolePermission]

    required_permission = "member.view"

    @extend_schema(
        responses={
            200: ReceptionDashboardSerializer,
        },
        tags=["Reception"],
        operation_id="reception_member_dashboard",
        summary="Get Member Reception Dashboard",
        description=(
            "Returns the complete reception dashboard "
            "information for a member."
        ),
    )
    def get(
        self,
        request,
        member_code,
    ):

        result = (
            ReceptionDashboardService
            .get_member_dashboard(
                member_code
            )
        )

        if not result["success"]:

            return Response(
                result,
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = ReceptionDashboardSerializer(
            result,
            context={"request": request},
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


# ==========================================================
# MEMBER SEARCH
# ==========================================================


class ReceptionSearchAPIView(APIView):

    permission_classes = [RolePermission]

    required_permission = "member.view"

    @extend_schema(
        responses={
            200: ReceptionSearchResponseSerializer,
        },
        tags=["Reception"],
        operation_id="reception_search_members",
        summary="Search Members",
        description=(
            "Searches members using the supplied "
            "search query."
        ),
    )
    def get(
        self,
        request,
    ):

        query = request.GET.get(
            "q",
            "",
        ).strip()

        if not query:

            return Response(
                {
                    "success": False,
                    "message": (
                        "Search query is required."
                    ),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        result = (
            ReceptionDashboardService
            .search_members(query)
        )

        serializer = (
            ReceptionSearchResponseSerializer(
                result
            )
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


# ==========================================================
# MEMBERSHIP RENEWAL
# ==========================================================


class ReceptionRenewAPIView(APIView):

    permission_classes = [RolePermission]

    required_permission = "membership.create"

    @extend_schema(
        request=MembershipRenewSerializer,
        responses={
            201: ReceptionRenewResponseSerializer,
        },
        tags=["Reception"],
        operation_id="reception_renew_membership",
        summary="Renew Membership",
        description=(
            "Renews a member's membership using "
            "the selected membership plan."
        ),
    )
    def post(
        self,
        request,
        member_code,
    ):

        serializer = MembershipRenewSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

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

            membership = (
                MembershipPurchaseService
                .purchase_membership(
                    member=member,
                    plan=plan,
                    start_date=timezone.now().date(),
                    amount_paid=data["amount_paid"],
                    payment_method=data[
                        "payment_method"
                    ],
                    transaction_id=data.get(
                        "transaction_id",
                        "",
                    ),
                    notes=(
                        "Reception Membership Renewal"
                    ),
                )
            )

            response_data = {
                "success": True,
                "message": (
                    "Membership renewed "
                    "successfully."
                ),
                "membership_id": membership.id,
                "status": membership.status,
                "start_date": membership.start_date,
                "end_date": membership.end_date,
            }

            response_serializer = (
                ReceptionRenewResponseSerializer(
                    response_data
                )
            )

            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED,
            )

        except ValueError as exc:

            return Response(
                {
                    "success": False,
                    "message": str(exc),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception:

            return Response(
                {
                    "success": False,
                    "message": (
                        "An unexpected error occurred "
                        "while processing the renewal."
                    ),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )