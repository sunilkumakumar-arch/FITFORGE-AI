from django.db.models import Count, Prefetch
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiResponse

from roles.permissions import RolePermission

from .models import (
    Trainer,
    TrainerWeeklyOff,
    TrainerCertification,
)

from .serializers import (
    TrainerSerializer,
    TrainerWeeklyOffSerializer,
    TrainerCertificationSerializer,
    TrainerCreateSerializer,
)

from trainer_assignments.models import TrainerAssignment


class TrainerViewSet(viewsets.ModelViewSet):

    queryset = Trainer.objects.all()

    serializer_class = TrainerSerializer

    permission_classes = [RolePermission]

    permission_map = {
        "list": "trainer.view",
        "retrieve": "trainer.view",
        "create": "trainer.create",
        "update": "trainer.update",
        "partial_update": "trainer.update",
        "destroy": "trainer.delete",
    }

    @action(detail=False, methods=["get"])
    def dashboard(self, request):

        total_trainers = Trainer.objects.count()

        active_trainers = Trainer.objects.filter(
            status="ACTIVE"
        ).count()

        inactive_trainers = Trainer.objects.exclude(
            status="ACTIVE"
        ).count()

        total_capacity = sum(
            trainer.trainer_capacity
            for trainer in Trainer.objects.filter(
                status="ACTIVE"
            )
        )

        occupied_capacity = TrainerAssignment.objects.filter(
            is_active=True,
            assignment_type="MEMBERSHIP"
        ).count()

        available_capacity = max(
            total_capacity - occupied_capacity,
            0
        )

        pt_clients = TrainerAssignment.objects.filter(
            is_active=True,
            assignment_type="PT"
        ).count()

        return Response({
            "total_trainers": total_trainers,
            "active_trainers": active_trainers,
            "inactive_trainers": inactive_trainers,
            "total_capacity": total_capacity,
            "occupied_capacity": occupied_capacity,
            "available_capacity": available_capacity,
            "pt_clients": pt_clients,
        })

    @action(detail=False, methods=["get"])
    def assignment_center(self, request):

        trainers = (
            Trainer.objects.prefetch_related(
                Prefetch(
                    "assignments",
                    queryset=TrainerAssignment.objects.filter(
                        is_active=True
                    ).select_related("member")
                )
            )
            .order_by("trainer_code")
        )

        data = []

        for trainer in trainers:

            assignments = trainer.assignments.all()

            membership_clients = []
            pt_clients = []

            for assignment in assignments:

                member_data = {
                    "id": assignment.member.id,
                    "name": (
                        f"{assignment.member.first_name} "
                        f"{assignment.member.last_name}"
                    ),
                    "assignment_id": assignment.id,
                }

                if assignment.assignment_type == "PT":
                    pt_clients.append(member_data)
                else:
                    membership_clients.append(member_data)

            occupied = len(assignments)

            available = max(
                trainer.trainer_capacity - occupied,
                0
            )

            data.append({
                "trainer_id": trainer.id,
                "trainer_code": trainer.trainer_code,
                "trainer_name":
                    f"{trainer.first_name} {trainer.last_name}",
                "employment_status":
                    trainer.employment_status,
                "trainer_status":
                    trainer.trainer_status,
                "capacity":
                    trainer.trainer_capacity,
                "occupied":
                    occupied,
                "available":
                    available,
                "membership_clients":
                    membership_clients,
                "pt_clients":
                    pt_clients,
            })

        return Response(data)

    def create(self, request, *args, **kwargs):

        return Response(
            {
                "detail":
                    "Use /api/v1/trainers/create/ to create trainers."
            },
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )


class TrainerCreateAPIView(APIView):

    permission_classes = [RolePermission]

    permission_map = {
        "list": "trainer.view",
        "retrieve": "trainer.view",
        "create": "trainer.create",
        "update": "trainer.update",
        "partial_update": "trainer.update",
        "destroy": "trainer.delete",
    }

    @extend_schema(
        request=TrainerCreateSerializer,
        responses={
            201: OpenApiResponse(
                response={
                    "type": "object",
                    "properties": {
                        "success": {
                            "type": "boolean"
                        },
                        "message": {
                            "type": "string"
                        },
                        "trainer_id": {
                            "type": "integer"
                        },
                        "trainer_code": {
                            "type": "string"
                        },
                    },
                },
                description="Trainer created successfully.",
            ),
        },
    )
    def post(self, request):

        serializer = TrainerCreateSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        trainer = serializer.save()

        return Response(
            {
                "success": True,
                "message": "Trainer created successfully.",
                "trainer_id": trainer.id,
                "trainer_code": trainer.trainer_code,
            },
            status=status.HTTP_201_CREATED,
        )


class TrainerWeeklyOffViewSet(
    viewsets.ModelViewSet
):

    queryset = (
        TrainerWeeklyOff.objects.all()
    )

    serializer_class = (
        TrainerWeeklyOffSerializer
    )

    permission_classes = [RolePermission]

    permission_map = {
        "list": "trainer.view",
        "retrieve": "trainer.view",
        "create": "trainer.create",
        "update": "trainer.update",
        "partial_update": "trainer.update",
        "destroy": "trainer.delete",
    }


class TrainerCertificationViewSet(
    viewsets.ModelViewSet
):
    """
    CRUD operations for Trainer Certifications.
    """

    queryset = TrainerCertification.objects.select_related(
        "trainer",
        "certification",
    )

    serializer_class = TrainerCertificationSerializer

    permission_classes = [RolePermission]

    permission_map = {
        "list": "trainer.view",
        "retrieve": "trainer.view",
        "create": "trainer.create",
        "update": "trainer.update",
        "partial_update": "trainer.update",
        "destroy": "trainer.delete",
    }