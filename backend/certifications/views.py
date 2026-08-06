from rest_framework import viewsets
from roles.permissions import RolePermission

from .models import Certification
from .serializers import CertificationSerializer


class CertificationViewSet(viewsets.ModelViewSet):
    queryset = Certification.objects.filter(is_active=True).order_by("name")
    serializer_class = CertificationSerializer
    permission_classes = [RolePermission]

    permission_map = {
        "list": "trainer.view",
        "retrieve": "trainer.view",
        "create": "trainer.create",
        "update": "trainer.update",
        "partial_update": "trainer.update",
        "destroy": "trainer.delete",
    }