from rest_framework import viewsets, status
from roles.permissions import RolePermission
from rest_framework.response import Response

from .models import Payment
from .serializers import PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):

    queryset = (
        Payment.objects
        .select_related(
            "member",
            "membership_plan",
        )
        .order_by("-payment_date", "-id")
    )

    serializer_class = PaymentSerializer

    permission_classes = [
        RolePermission
    ]

    permission_map = {
        "list": "billing.view",
        "retrieve": "billing.view",
        "create": "billing.create",
        "update": "billing.update",
        "partial_update": "billing.update",
        "destroy": "billing.delete",
    }

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        payment = serializer.save()

        return Response(
            PaymentSerializer(payment).data,
            status=status.HTTP_201_CREATED,
        )