from django.db.models import Sum

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from memberships.models import MemberMembership

from .models import Payment
from .serializers import PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):

    queryset = Payment.objects.select_related(
        "member",
        "membership_plan",
    )

    serializer_class = PaymentSerializer

    permission_classes = [
        IsAuthenticated
    ]

    @action(
        detail=False,
        methods=["get"]
    )
    def total_revenue(self, request):

        revenue = (
            MemberMembership.objects.aggregate(
                total=Sum("amount_paid")
            )["total"]
            or 0
        )

        return Response({
            "total_revenue": revenue
        })