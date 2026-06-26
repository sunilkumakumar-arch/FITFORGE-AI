from rest_framework import viewsets
from .models import MembershipPlan, MemberMembership
from .serializers import (
    MembershipPlanSerializer,
    MemberMembershipSerializer,
)


class MembershipPlanViewSet(viewsets.ModelViewSet):
    queryset = MembershipPlan.objects.all()
    serializer_class = MembershipPlanSerializer


class MemberMembershipViewSet(viewsets.ModelViewSet):
    queryset = MemberMembership.objects.all()
    serializer_class = MemberMembershipSerializer