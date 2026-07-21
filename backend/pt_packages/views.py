from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from django.utils import timezone

from memberships.models import MemberMembership

from .models import (
    PTPackage,
    MemberPTPackage,
    PTSession,
)

from .serializers import (
    PTPackageSerializer,
    MemberPTPackageSerializer,
    PTSessionSerializer,
)
from billing.models import Payment
from decimal import Decimal


class PTPackageViewSet(
    viewsets.ModelViewSet
):

    serializer_class = (
        PTPackageSerializer
    )

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):
        return (
            PTPackage.objects
            .filter(is_active=True)
            .order_by("name")
        )

    @action(
        detail=True,
        methods=["patch"],
    )
    def deactivate(
        self,
        request,
        pk=None,
    ):
        package = self.get_object()

        package.is_active = False

        package.save()

        return Response(
            {
                "message":
                "Package deactivated successfully"
            },
            status=status.HTTP_200_OK,
        )


class MemberPTPackageViewSet(
    viewsets.ModelViewSet
):

    queryset = (
        MemberPTPackage.objects
        .select_related(
            "member",
            "package",
            "trainer_assignment",
        )
        .all()
    )

    serializer_class = (
        MemberPTPackageSerializer
    )

    permission_classes = [
        IsAuthenticated
    ]

    def perform_create(
        self,
        serializer,
    ):

        member = serializer.validated_data.get(
            "member"
        )

        if not member:
            raise ValidationError(
                {
                    "error":
                    "Member information missing."
                }
            )

        active_membership = (
            MemberMembership.objects
            .filter(
                member=member,
                status="Active",
            )
            .order_by("-end_date")
            .first()
        )

        if not active_membership:
            raise ValidationError(
                {
                    "error":
                    "Active membership required before purchasing a PT Package."
                }
            )

        remaining_membership_days = (
            active_membership.end_date -
            timezone.now().date()
        ).days

        if remaining_membership_days <= 0:
            raise ValidationError(
                {
                    "error":
                    "Membership has expired. Renew membership first."
                }
            )

        active_package = (
            MemberPTPackage.objects
            .filter(
                member=member,
                is_active=True,
            )
            .order_by("-expiry_date")
            .first()
        )

        if active_package:

            remaining_sessions = (
                active_package.package.total_sessions -
                active_package.sessions_used
            )

            remaining_days = (
                active_package.expiry_date -
                timezone.now().date()
            ).days

            if (
                remaining_sessions > 3 and
                remaining_days > 15
            ):
                raise ValidationError(
                    {
                        "error":
                        f"Active PT Package already exists. Remaining Sessions: {remaining_sessions}, Remaining Days: {remaining_days}"
                    }
                )

        package_instance = serializer.save()

        if (
            package_instance.expiry_date >
            active_membership.end_date
        ):
            package_instance.expiry_date = (
                active_membership.end_date
            )

            package_instance.save()

        Payment.objects.create(
            member=member,
            membership_plan=None,
            amount=package_instance.package.price,
            payment_method="Cash",
            payment_status="Paid",
            transaction_id="",
            notes=(
                f"PT Package Purchase - "
                f"{package_instance.package.name}"
            ),
        )    


class PTSessionViewSet(
    viewsets.ModelViewSet
):

    queryset = (
        PTSession.objects
        .select_related(
            "member_package",
            "trainer",
        )
        .all()
    )

    serializer_class = (
        PTSessionSerializer
    )

    permission_classes = [
        IsAuthenticated
    ]