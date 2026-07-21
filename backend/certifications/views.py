from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Certification
from .serializers import CertificationSerializer


class CertificationViewSet(viewsets.ModelViewSet):
    queryset = Certification.objects.filter(is_active=True).order_by("name")
    serializer_class = CertificationSerializer
    permission_classes = [IsAuthenticated]