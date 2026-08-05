from .models import (
    GeneralTrainerAssignment,
    GeneralTrainerChangeHistory,
)


class GeneralTrainingSelector:
    @staticmethod
    def get_current_assignment(member):
        return (
            GeneralTrainerAssignment.objects
            .filter(
                member=member,
                assignment_status=GeneralTrainerAssignment.AssignmentStatus.ACTIVE,
            )
            .select_related(
                "member",
                "trainer",
                "membership",
            )
            .first()
        )

    @staticmethod
    def get_assignment_history(member):
        return (
            GeneralTrainerAssignment.objects
            .filter(member=member)
            .select_related(
                "trainer",
                "membership",
            )
            .order_by("-created_at")
        )

    @staticmethod
    def get_trainer_members(trainer):
        return (
            GeneralTrainerAssignment.objects
            .filter(
                trainer=trainer,
                assignment_status=GeneralTrainerAssignment.AssignmentStatus.ACTIVE,
            )
            .select_related(
                "member",
                "membership",
            )
        )

    @staticmethod
    def get_change_history(member):
        return (
            GeneralTrainerChangeHistory.objects
            .filter(member=member)
            .select_related(
                "old_trainer",
                "new_trainer",
            )
            .order_by("-changed_at")
        )