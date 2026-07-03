from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

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
    permission_classes = [IsAuthenticated]


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
    permission_classes = [IsAuthenticated]