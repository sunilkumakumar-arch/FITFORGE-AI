from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response

from roles.permissions import RolePermission

from .models import (
    MembershipPlan,
    MemberMembership,
)
from .purchase_serializer import PurchaseMembershipSerializer
from .serializers import (
    MembershipPlanSerializer,
    MemberMembershipSerializer,
)
from .services import MembershipPurchaseService


class MembershipPlanViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoints for Membership Plan Management.
    """

    queryset = MembershipPlan.objects.all()

    serializer_class = MembershipPlanSerializer

    permission_classes = [
        RolePermission,
    ]

    permission_map = {
        "list": "membership.view",
        "retrieve": "membership.view",
    }

    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )

    filterset_fields = (
        "organization",
        "branch",
        "is_active",
        "duration_days",
    )

    search_fields = (
        "name",
        "code",
        "description",
    )

    ordering_fields = (
        "name",
        "code",
        "price",
        "duration_days",
        "created_at",
        "updated_at",
    )

    ordering = (
        "name",
    )

    def get_queryset(self):
        return (
            MembershipPlan.objects
            .select_related(
                "organization",
                "branch",
            )
            .filter(is_active=True)
            .order_by("name")
        )


class MemberMembershipViewSet(viewsets.ModelViewSet):
    """
    Enterprise Membership Management API.
    """

    queryset = (
        MemberMembership.objects
        .select_related(
            "member",
            "plan",
            "plan__organization",
            "plan__branch",
        )
        .order_by("-created_at")
    )

    serializer_class = MemberMembershipSerializer

    permission_classes = [
        RolePermission,
    ]

    permission_map = {
        "list": "membership.view",
        "retrieve": "membership.view",
        "create": "membership.create",
        "purchase": "membership.create",
        "update": "membership.update",
        "partial_update": "membership.update",
        "destroy": "membership.delete",
    }

    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )

    filterset_fields = (
        "member",
        "plan",
        "status",
        "start_date",
        "end_date",
        "plan__organization",
        "plan__branch",
    )

    search_fields = (
        "member__first_name",
        "member__last_name",
        "member__phone",
        "plan__name",
        "plan__code",
        "payment_reference",
    )

    ordering_fields = (
        "start_date",
        "end_date",
        "amount_paid",
        "created_at",
        "updated_at",
    )

    ordering = (
        "-created_at",
    )

    @action(
        detail=False,
        methods=["post"],
        url_path="purchase",
    )
    def purchase(self, request):

        serializer = PurchaseMembershipSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        data = serializer.validated_data

        membership = MembershipPurchaseService.purchase_membership(
            member=data["member"],
            plan=data["plan"],
            start_date=data["start_date"],
            amount_paid=data["amount_paid"],
            payment_method=data["payment_method"],
            transaction_id=data.get(
                "transaction_id",
                "",
            ),
            notes=data.get(
                "notes",
                "",
            ),
        )

        return Response(
            MemberMembershipSerializer(
                membership
            ).data,
            status=status.HTTP_201_CREATED,
        )