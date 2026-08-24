from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from drf_spectacular.utils import extend_schema

from roles.permissions import RolePermission

from .services import MembershipPurchaseService
from .purchase_serializer import PurchaseMembershipSerializer
from .serializers import MemberMembershipSerializer


class MembershipPurchaseView(APIView):
    """
    Purchase a membership for a member.
    """

    permission_classes = [RolePermission]

    required_permission = "membership.create"

    @extend_schema(
        request=PurchaseMembershipSerializer,
        responses={
            201: MemberMembershipSerializer,
        },
        tags=["Memberships"],
        operation_id="purchase_membership",
        summary="Purchase Membership",
        description=(
            "Creates a new membership for a member, "
            "records the payment details, and returns "
            "the created membership."
        ),
    )
    def post(self, request):

        serializer = PurchaseMembershipSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        data = serializer.validated_data

        membership = (
            MembershipPurchaseService.purchase_membership(
                member=data["member"],
                plan=data["plan"],
                start_date=data.get(
                    "start_date",
                    timezone.now().date(),
                ),
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
        )

        response_serializer = MemberMembershipSerializer(
            membership,
            context={"request": request},
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )