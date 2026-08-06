from datetime import date

from rest_framework import viewsets
from roles.permissions import RolePermission
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import TrainerAssignment
from .serializers import TrainerAssignmentSerializer
from .services import TrainerAssignmentService

from trainers.models import Trainer


class TrainerAssignmentViewSet(
    viewsets.ModelViewSet
):

    queryset = TrainerAssignment.objects.all()

    serializer_class = TrainerAssignmentSerializer

    permission_classes = [RolePermission]

    permission_map = {
        "list": "trainer.view",
        "retrieve": "trainer.view",
        "create": "trainer.create",
        "update": "trainer.update",
        "partial_update": "trainer.update",
        "destroy": "trainer.delete",

        "available_trainers": "trainer.view",
        "auto_assign": "trainer.update",
        "change_trainer": "trainer.update",
        "create_assignment": "trainer.create",
    }

    # =====================================
    # AVAILABLE TRAINERS
    # =====================================

    def is_trainer_available_for_time(
        self,
        trainer,
        slot_time
    ):
        try:

            hour = int(
                slot_time.split(":")[0]
            )

            minute = int(
                slot_time.split(":")[1]
            )

            total_minutes = (
                hour * 60
            ) + minute

            shift_map = {

                "SHIFT_1": [
                    (360, 630),   # 6:00 AM - 10:30 AM
                    (1020, 1290), # 5:00 PM - 9:30 PM
                ],

                "SHIFT_2": [
                    (360, 630),   # 6:00 AM - 10:30 AM
                    (1050, 1320), # 5:30 PM - 10:00 PM
                ],

                "SHIFT_3": [
                    (360, 900),   # 6:00 AM - 3:00 PM
                ],

                "SHIFT_4": [
                    (780, 1320),  # 1:00 PM - 10:00 PM
                ],

                "SHIFT_5": [
                    (330, 930),   # 5:30 AM - 3:30 PM
                ],

                "SHIFT_6": [
                    (720, 1260),  # 12:00 PM - 9:00 PM
                ],
            }

            trainer_shifts = shift_map.get(
                trainer.shift_type,
                []
            )

            for start_time, end_time in trainer_shifts:

                if (
                    total_minutes >= start_time and
                    total_minutes <= end_time
                ):
                    return True

            return False

        except Exception:
            return False


    def is_trainer_available_for_time(
        self,
        trainer,
        slot_time
    ):

        try:

            parts = slot_time.split(":")

            hour = int(parts[0])
            minute = int(parts[1])

            total_minutes = (
                hour * 60
            ) + minute

            shift = trainer.shift_type

            # SHIFT 1
            if shift == "SHIFT_1":

                morning = (
                    360 <= total_minutes <= 630
                )

                evening = (
                    1020 <= total_minutes <= 1290
                )

                return morning or evening

            # SHIFT 2
            if shift == "SHIFT_2":

                morning = (
                    360 <= total_minutes <= 630
                )

                evening = (
                    1050 <= total_minutes <= 1320
                )

                return morning or evening

            # SHIFT 3
            if shift == "SHIFT_3":

                return (
                    360 <= total_minutes <= 900
                )

            # SHIFT 4
            if shift == "SHIFT_4":

                return (
                    780 <= total_minutes <= 1320
                )

            # SHIFT 5
            if shift == "SHIFT_5":

                return (
                    330 <= total_minutes <= 930
                )

            # SHIFT 6
            if shift == "SHIFT_6":

                return (
                    720 <= total_minutes <= 1260
                )

            return False

        except Exception:
            return False
    
    
    @action(
        detail=False,
        methods=["get"],
        url_path="available-trainers"
    )
    def available_trainers(self, request):

        goal_type = request.GET.get("goal_type")

        slot_time = request.GET.get("slot_time")

        trainers = TrainerAssignmentService.get_available_trainers(
            goal_type=goal_type,
            slot_time=slot_time,
        )

        return Response(trainers)

    # =====================================
    # AUTO ASSIGN TRAINER
    # =====================================

    @action(
        detail=False,
        methods=["post"],
        url_path="auto-assign"
    )
    def auto_assign(self, request):

        goal_type = request.data.get(
            "goal_type"
        )

        slot_time = request.data.get(
            "slot_time"
        )

        trainers = Trainer.objects.filter(
            employment_status="Active",
            available_for_pt=True
        )

        candidates = []

        for trainer in trainers:

            current_member_count = (
                TrainerAssignment.objects
                .filter(
                    trainer=trainer,
                    is_active=True,
                    assignment_type="MEMBERSHIP"
                )
                .count()
            )

            if current_member_count >= trainer.trainer_capacity:
                continue

            if not self.is_trainer_available_for_time(
                trainer,
                slot_time
            ):
                continue

            current_assignments = (
                TrainerAssignment.objects
                .filter(
                    trainer=trainer,
                    slot_time=slot_time,
                    is_active=True,
                    assignment_type="PT"
                )
            )

            if current_assignments.count() >= 2:
                continue

            existing_goals = set(
                current_assignments.values_list(
                    "goal_type",
                    flat=True
                )
            )

            existing_goals.discard(None)

            if (
                existing_goals and
                goal_type not in existing_goals
            ):
                continue

            current_member_count = (
                TrainerAssignment.objects.filter(
                    trainer=trainer,
                    is_active=True,
                    assignment_type="MEMBERSHIP"
                ).count()
            )

            remaining_capacity = (
                trainer.trainer_capacity -
                current_member_count
            )

            candidates.append({
                "trainer": trainer,
                "current_members":
                    current_member_count,
                "remaining_capacity":
                    remaining_capacity,
                "trainer_level":
                    trainer.trainer_level,
            })

            if not candidates:

                return Response(
                    {
                        "success": False,
                        "message":
                            "No trainer available for selected slot."
                    },
                    status=400
                )

            candidates = sorted(
                candidates,
                key=lambda x: (
                    x["current_members"],
                    -x["remaining_capacity"],
                    x["trainer_level"]
                )
            )

            selected = candidates[0]["trainer"]

        

        return Response({
            "success": True,
            "trainer_id":
                selected.id,
            "trainer_code":
                selected.trainer_code,
            "trainer_name":
                f"{selected.first_name} {selected.last_name}",
            "trainer_level":
                selected.trainer_level,
            "experience_years":
                selected.experience_years,
            "specialization":
                selected.specialization,
            "rating":
                selected.rating,
            "shift_type":
                selected.shift_type,
            "message":
                "Trainer assigned automatically."
        })

    # =====================================
    # CHANGE TRAINER
    # =====================================

    @action(
        detail=False,
        methods=["post"],
        url_path="change-trainer"
    )
    def change_trainer(self, request):

        member_id = request.data.get(
            "member_id"
        )

        new_trainer_id = request.data.get(
            "trainer_id"
        )

        goal_type = request.data.get(
            "goal_type",
            "GENERAL_FITNESS"
        )

        slot_time = request.data.get(
            "slot_time"
        )

        day_pattern = request.data.get(
            "day_pattern",
            "MWF"
        )

        current_assignment = (
            TrainerAssignment.objects
            .filter(
                member_id=member_id,
                is_active=True
            )
            .order_by("-created_at")
            .first()
        )

        if current_assignment:

            current_assignment.is_active = False
            current_assignment.save()

        new_assignment = (
            TrainerAssignment.objects.create(
                trainer_id=new_trainer_id,
                member_id=member_id,
                start_date=date.today(),
                monthly_fee=0,
                sessions_per_week=3,
                assignment_type="PT",
                package_type="3_DAYS",
                goal_type=goal_type,
                slot_time=slot_time,
                day_pattern=day_pattern,
                auto_assigned=False,
                is_active=True,
            )
        )

        return Response({
            "success": True,
            "assignment_id":
                new_assignment.id,
            "message":
                "Trainer changed successfully."
        })

    # =====================================
    # CREATE ASSIGNMENT
    # =====================================

    @action(
        detail=False,
        methods=["post"],
        url_path="create-assignment"
    )
    def create_assignment(self, request):

        serializer = (
            TrainerAssignmentSerializer(
                data=request.data
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        assignment = serializer.save()

        return Response(
            {
                "success": True,
                "assignment_id":
                    assignment.id,
                "message":
                    "Trainer assignment created successfully."
            }
        )