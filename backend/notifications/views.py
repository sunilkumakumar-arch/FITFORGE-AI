from rest_framework import viewsets
from roles.permissions import RolePermission

from .models import Notification
from .serializers import NotificationSerializer


class NotificationViewSet(viewsets.ModelViewSet):

    queryset = Notification.objects.all()

    serializer_class = NotificationSerializer

    permission_classes = [RolePermission]

    permission_map = {
        "list": "member.view",
        "retrieve": "member.view",
        "create": "member.update",
        "update": "member.update",
        "partial_update": "member.update",
        "destroy": "member.delete",
    }