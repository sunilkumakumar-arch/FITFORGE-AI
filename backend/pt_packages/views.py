from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import (
    PTPackage,
    MemberPTPackage,
    PTSession,
)

from .serializers import (
    PTPackageSerializer,
    MemberPTPackageSerializer,
    PTSessionSerializer,
)


class PTPackageViewSet(
    viewsets.ModelViewSet
):

    serializer_class = (
        PTPackageSerializer
    )

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):
        return (
            PTPackage.objects
            .filter(is_active=True)
            .order_by("name")
        )

    @action(
        detail=True,
        methods=["patch"],
    )
    def deactivate(
        self,
        request,
        pk=None,
    ):
        package = self.get_object()

        package.is_active = False

        package.save()

        return Response(
            {
                "message":
                "Package deactivated successfully"
            },
            status=status.HTTP_200_OK,
        )


class MemberPTPackageViewSet(
    viewsets.ModelViewSet
):

    queryset = (
        MemberPTPackage.objects
        .select_related(
            "member",
            "package",
            "trainer_assignment",
        )
        .all()
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

    queryset = (
        PTSession.objects
        .select_related(
            "member_package",
            "trainer",
        )
        .all()
    )

    serializer_class = (
        PTSessionSerializer
    )

    permission_classes = [
        IsAuthenticated
    ]