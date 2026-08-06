from roles.permissions import RolePermission

from .services import MembershipPurchaseService
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from .purchase_serializer import PurchaseMembershipSerializer

from .models import (
    MembershipPlan,
    MemberMembership,
)

from .serializers import (
    MembershipPlanSerializer,
    MemberMembershipSerializer,
)

from rest_framework import viewsets

class MembershipPlanViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = MembershipPlan.objects.all()

    serializer_class = MembershipPlanSerializer

    permission_classes = [
        RolePermission
    ]
    permission_map = {
        "list": "membership.view",
        "retrieve": "membership.view",
    }

    def get_queryset(self):
        return (
            MembershipPlan.objects
            .filter(is_active=True)
            .order_by("name")
        )


class MemberMembershipViewSet(viewsets.ModelViewSet):

    queryset = (
        MemberMembership.objects
        .select_related(
            "member",
            "plan"
        )
        .order_by("-created_at")
    )

    serializer_class = MemberMembershipSerializer

    permission_classes = [
        RolePermission
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

    


    @action(
        detail=False,
        methods=["post"],
        url_path="purchase",
    )
    def purchase(self, request):

        serializer = PurchaseMembershipSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        membership = MembershipPurchaseService.purchase_membership(
            member=data["member"],
            plan=data["plan"],
            start_date=data["start_date"],
            amount_paid=data["amount_paid"],
            payment_method=data["payment_method"],
            transaction_id=data.get("transaction_id", ""),
            notes=data.get("notes", ""),
        )

        return Response(
            MemberMembershipSerializer(membership).data,
            status=status.HTTP_201_CREATED,
        )    