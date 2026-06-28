from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Trainer
from .serializers import TrainerSerializer


class TrainerViewSet(viewsets.ModelViewSet):

    queryset = Trainer.objects.all()

    serializer_class = TrainerSerializer

    permission_classes = [IsAuthenticated]