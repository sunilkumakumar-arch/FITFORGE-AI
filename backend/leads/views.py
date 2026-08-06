# leads/views.py

from rest_framework import viewsets
from roles.permissions import RolePermission

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

    permission_classes = [RolePermission]

    permission_map = { 
        "list": "member.view",
        "retrieve": "member.view",
        "create": "member.create",
        "update": "member.update",
        "partial_update": "member.update",
        "destroy": "member.delete",
    }


class LeadFollowUpViewSet(
    viewsets.ModelViewSet
):

    queryset = LeadFollowUp.objects.all()

    serializer_class = (
        LeadFollowUpSerializer
    )

    permission_classes = [RolePermission]

    permission_map = {
        "list": "member.view",
        "retrieve": "member.view",
        "create": "member.create",
        "update": "member.update",
        "partial_update": "member.update",
        "destroy": "member.delete",
    }