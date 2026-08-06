from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from roles.permissions import RolePermission
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Member

from trainers.models import Trainer

from .services import (
    PTPackagePurchaseService,
    PTTrainerAssignmentService,
)

from .serializers import (
    PTPackageSerializer,
    MemberPTPackageSerializer,
    PTSessionSerializer,
    PTPackagePurchaseSerializer,
    PTAssignTrainerSerializer,
)


from .models import (
    PTPackage,
    MemberPTPackage,
    PTSession,
)



from .services import PTPackagePurchaseService


class PTPackageViewSet(viewsets.ModelViewSet):
    serializer_class = PTPackageSerializer
    permission_classes = [RolePermission]

    permission_map = { 
        "list": "membership.view",
        "retrieve": "membership.view",
        "create": "membership.create",
        "update": "membership.update",
        "partial_update": "membership.update",
        "destroy": "membership.delete",
        "deactivate": "membership.update",
    }

    def get_queryset(self):
        return (
            PTPackage.objects
            .filter(is_active=True)
            .order_by("name")
        )

    @action(detail=True, methods=["patch"])
    def deactivate(self, request, pk=None):
        package = self.get_object()

        package.is_active = False
        package.save(update_fields=["is_active"])

        return Response(
            {
                "message": "Package deactivated successfully",
            },
            status=status.HTTP_200_OK,
        )


class MemberPTPackageViewSet(viewsets.ModelViewSet):
    queryset = (
        MemberPTPackage.objects
        .select_related(
            "member",
            "package",
            "trainer_assignment",
        )
        .all()
    )

    serializer_class = MemberPTPackageSerializer
    permission_classes = [RolePermission]

    permission_map = {
        "list": "membership.view",
        "retrieve": "membership.view",
        
        "update": "membership.update",
        "partial_update": "membership.update",
        "destroy": "membership.delete",
        
    }

    def create(self, request, *args, **kwargs):
        return Response(
            {
                "success": False,
                "message": (
                    "Direct PT Package creation is not allowed. "
                    "Use the /purchase/ endpoint."
                ),
            },
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def perform_create(self, serializer):
        data = serializer.validated_data

        PTPackagePurchaseService.purchase_package(
            member=data["member"],
            package=data["package"],
            amount_paid=data["package"].price,
            payment_method="Cash",
            transaction_id="",
            notes=f"PT Package Purchase - {data['package'].name}",
        )


class PTPackagePurchaseAPIView(APIView):
    permission_classes = [RolePermission]

    required_permission = "membership.create"

    def post(self, request):

        serializer = PTPackagePurchaseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        member = get_object_or_404(
            Member,
            member_code=data["member_code"],
        )

        

        package = get_object_or_404(
            PTPackage,
            id=data["package_id"],
            is_active=True,
        )

        try:
            member_package = PTPackagePurchaseService.purchase_package(
                member=member,
                package=package,
                amount_paid=data["amount_paid"],
                payment_method=data["payment_method"],
                transaction_id=data.get("transaction_id", ""),
                notes=f"PT Package Purchase - {package.name}",
            )

            return Response(
                {
                    "success": True,
                    "message": "PT Package purchased successfully.",
                    "member_package_id": member_package.id,
                    "package": package.name,
                    "total_sessions": package.total_sessions,
                    "remaining_sessions": member_package.sessions_remaining,
                    "expiry_date": member_package.expiry_date.isoformat(),
                },
                status=status.HTTP_201_CREATED,
            )

        except ValidationError as e:
            return Response(
                {
                    "success": False,
                    "message": str(e.detail),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": "An unexpected error occurred while purchasing the PT package.",
                    "error": str(e),  # Remove in production if desired
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class PTAssignTrainerAPIView(APIView):
    permission_classes = [RolePermission]

    required_permission = "trainer.update"

    def post(self, request):

        serializer = PTAssignTrainerSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        member_package = get_object_or_404(
            MemberPTPackage,
            id=data["member_package_id"],
            is_active=True,
        )

        trainer = get_object_or_404(
            Trainer,
            id=data["trainer_id"],
        )

        try:

            trainer_assignment = (
                PTTrainerAssignmentService.assign_trainer(
                    member_package=member_package,
                    trainer=trainer,
                )
            )

            return Response(
                {
                    "success": True,
                    "message": (
                        "Trainer assigned successfully."
                    ),
                    "trainer_assignment_id": (
                        trainer_assignment.id
                    ),
                    "member": (
                        member_package.member.member_code
                    ),
                    "trainer": (
                        trainer.first_name
                    ),
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:

            return Response(
                {
                    "success": False,
                    "message": (
                        "Unable to assign trainer."
                    ),
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )        


class PTSessionViewSet(viewsets.ModelViewSet):
    queryset = (
        PTSession.objects
        .select_related(
            "member_package",
            "trainer",
        )
        .all()
    )

    serializer_class = PTSessionSerializer
    permission_classes = [RolePermission]

    permission_map = {
        "list": "trainer.view",
        "retrieve": "trainer.view",
        "create": "trainer.update",
        "update": "trainer.update",
        "partial_update": "trainer.update",
        "destroy": "trainer.delete",
    }
