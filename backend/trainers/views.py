from django.db.models import Count, Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Prefetch, Sum
from rest_framework import status
from rest_framework.views import APIView

from .serializers import TrainerCreateSerializer

from .models import (
    Trainer,
    TrainerWeeklyOff,
)

from .serializers import (
    TrainerSerializer,
    TrainerWeeklyOffSerializer,
)

from trainer_assignments.models import TrainerAssignment
from .models import TrainerCertification
from .serializers import TrainerCertificationSerializer

class TrainerViewSet(viewsets.ModelViewSet):

    queryset = Trainer.objects.all()

    serializer_class = TrainerSerializer

    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get"])
    def dashboard(self, request):

        total_trainers = Trainer.objects.count()

        active_trainers = Trainer.objects.filter(
            status="ACTIVE"
        ).count()

        inactive_trainers = Trainer.objects.exclude(
            status="ACTIVE"
        ).count()

        total_capacity = (
            Trainer.objects.filter(
                status="ACTIVE"
            )
            .aggregate(
                total=Count("id")
            )
        )

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

    permission_classes = [IsAuthenticated]

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

    permission_classes = [
        IsAuthenticated
    ]

    

class TrainerCertificationViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for Trainer Certifications.
    """

    queryset = TrainerCertification.objects.select_related(
        "trainer",
        "certification",
    )

    serializer_class = TrainerCertificationSerializer
    permission_classes = [IsAuthenticated]