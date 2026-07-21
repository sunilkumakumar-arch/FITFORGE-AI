from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from .services import MembershipPurchaseService

from .models import (
    MembershipPlan,
    MemberMembership,
)

from .serializers import (
    MembershipPlanSerializer,
    MemberMembershipSerializer,
)


class MembershipPlanViewSet(viewsets.ModelViewSet):

    queryset = MembershipPlan.objects.all()

    serializer_class = MembershipPlanSerializer

    permission_classes = [
        IsAuthenticated
    ]

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
        .all()
    )

    serializer_class = MemberMembershipSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def perform_create(self, serializer):

        try:
            membership = MembershipPurchaseService.purchase_membership(
                member=serializer.validated_data["member"],
                plan=serializer.validated_data["plan"],
                start_date=serializer.validated_data["start_date"],
                amount_paid=serializer.validated_data["amount_paid"],
                payment_method="Cash",
                transaction_id="",
                notes="Membership Purchase",
            )

            print(f"Membership Created ID: {membership.id}")
            print(f"Member ID: {membership.member.id}")
            print(f"Plan ID: {membership.plan.id}")


            serializer.instance = membership

        except ValueError as e:
            raise ValidationError(
                {
                    "error": str(e)
                }
            )