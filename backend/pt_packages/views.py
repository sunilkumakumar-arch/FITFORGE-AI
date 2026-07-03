from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import (
    PTPackage,
    MemberPTPackage,
    PTSession
)

from .serializers import (
    PTPackageSerializer,
    MemberPTPackageSerializer,
    PTSessionSerializer
)


class PTPackageViewSet(
    viewsets.ModelViewSet
):

    queryset = PTPackage.objects.all()

    serializer_class = (
        PTPackageSerializer
    )

    permission_classes = [
        IsAuthenticated
    ]


class MemberPTPackageViewSet(
    viewsets.ModelViewSet
):

    queryset = (
        MemberPTPackage.objects.all()
    )

    serializer_class = (
        MemberPTPackageSerializer
    )

    permission_classes = [
        IsAuthenticated
    ]


class PTSessionViewSet(
    viewsets.ModelViewSet
):

    queryset = PTSession.objects.all()

    serializer_class = (
        PTSessionSerializer
    )

    permission_classes = [
        IsAuthenticated
    ]