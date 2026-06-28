from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import TrainerAssignment
from .serializers import TrainerAssignmentSerializer


class TrainerAssignmentViewSet(
    viewsets.ModelViewSet
):

    queryset = TrainerAssignment.objects.all()

    serializer_class = TrainerAssignmentSerializer

    permission_classes = [IsAuthenticated]