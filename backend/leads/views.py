# leads/views.py

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import (
    Lead,
    LeadFollowUp
)

from .serializers import (
    LeadSerializer,
    LeadFollowUpSerializer
)


class LeadViewSet(
    viewsets.ModelViewSet
):

    queryset = Lead.objects.all()

    serializer_class = LeadSerializer

    permission_classes = [
        IsAuthenticated
    ]


class LeadFollowUpViewSet(
    viewsets.ModelViewSet
):

    queryset = LeadFollowUp.objects.all()

    serializer_class = (
        LeadFollowUpSerializer
    )

    permission_classes = [
        IsAuthenticated
    ]