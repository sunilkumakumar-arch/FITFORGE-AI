from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response

from roles.permissions import RolePermission

from .models import Payment
from .serializers import PaymentSerializer
from .services import PaymentService


class PaymentViewSet(viewsets.ModelViewSet):
    """
    Enterprise Payment Management API.
    """

    queryset = (
        Payment.objects
        .select_related(
            "member",
            "membership",
            "membership__plan",
            "organization",
            "branch",
            "collected_by",
        )
        .order_by("-payment_date", "-id")
    )

    serializer_class = PaymentSerializer

    permission_classes = [
        RolePermission,
    ]

    permission_map = {
        "list": "billing.view",
        "retrieve": "billing.view",
        "create": "billing.create",
        "update": "billing.update",
        "partial_update": "billing.update",
        "destroy": "billing.delete",
    }

    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )

    filterset_fields = (
        "organization",
        "branch",
        "member",
        "membership",
        "payment_status",
        "payment_method",
        "payment_date",
    )

    search_fields = (
        "payment_number",
        "invoice_number",
        "receipt_number",
        "transaction_id",
        "member__first_name",
        "member__last_name",
        "member__phone",
    )

    ordering_fields = (
        "payment_date",
        "created_at",
        "final_amount",
        "amount",
        "payment_number",
    )

    ordering = (
        "-payment_date",
        "-id",
    )

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        payment = PaymentService.create_payment(
            **serializer.validated_data
        )

        return Response(
            self.get_serializer(payment).data,
            status=status.HTTP_201_CREATED,
        )