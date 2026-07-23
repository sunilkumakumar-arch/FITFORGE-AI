from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from accounts.models import Member

from .models import MembershipPlan
from .services import MembershipPurchaseService
from .purchase_serializer import PurchaseMembershipSerializer
from .serializers import MemberMembershipSerializer


class MembershipPurchaseView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = PurchaseMembershipSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        membership = MembershipPurchaseService.purchase_membership(
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

        return Response(
            MemberMembershipSerializer(
                membership
            ).data,
            status=status.HTTP_201_CREATED,
        )