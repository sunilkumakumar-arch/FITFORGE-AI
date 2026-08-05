from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from shared.trainer.services import TrainerStatisticsService
from .models import GeneralTrainerAssignment, GeneralTrainerChangeHistory
from .selectors import GeneralTrainingSelector


class GeneralTrainingService:

    @staticmethod
    @transaction.atomic
    def assign_trainer(*, member, membership, trainer, assigned_by=None,
                       assignment_mode=GeneralTrainerAssignment.AssignmentMode.MANUAL,
                       notes=""):
        if membership.member_id != member.id:
            raise ValidationError({"membership":"Selected membership does not belong to the member."})
        if membership.status != "Active":
            raise ValidationError({"membership":"Only active memberships can have a General Trainer."})
        if trainer.employment_status != "Active":
            raise ValidationError({"trainer":"Only active trainers can be assigned."})
        if GeneralTrainingSelector.get_current_assignment(member):
            raise ValidationError({"member":"Member already has an active General Trainer."})

        assignment = GeneralTrainerAssignment.objects.create(
            member=member,
            membership=membership,
            trainer=trainer,
            assignment_status=GeneralTrainerAssignment.AssignmentStatus.ACTIVE,
            assignment_mode=assignment_mode,
            start_date=membership.start_date,
            assigned_by=assigned_by,
            notes=notes,
        )
        TrainerStatisticsService.increment_active_clients(trainer)
        return assignment

    @staticmethod
    @transaction.atomic
    def close_assignment(*, assignment,
                         status=GeneralTrainerAssignment.AssignmentStatus.COMPLETED):
        if assignment.assignment_status != GeneralTrainerAssignment.AssignmentStatus.ACTIVE:
            raise ValidationError({"assignment":"Only active assignments can be closed."})
        assignment.assignment_status = status
        assignment.end_date = timezone.now().date()
        assignment.save(update_fields=["assignment_status","end_date","updated_at"])
        TrainerStatisticsService.decrement_active_clients(assignment.trainer)
        return assignment

    @staticmethod
    def _create_change_history(*, assignment, new_trainer, reason, rating,
                               comments="", changed_by=None):
        return GeneralTrainerChangeHistory.objects.create(
            assignment=assignment,
            member=assignment.member,
            old_trainer=assignment.trainer,
            new_trainer=new_trainer,
            reason=reason,
            rating=rating,
            comments=comments,
            changed_by=changed_by,
        )

    @staticmethod
    @transaction.atomic
    def change_trainer(*, member, new_trainer, reason, rating,
                       changed_by=None, comments=""):
        current = GeneralTrainingSelector.get_current_assignment(member)
        if not current:
            raise ValidationError({"member":"No active General Trainer assignment found."})
        if current.trainer_id == new_trainer.id:
            raise ValidationError({"trainer":"Selected trainer is already assigned."})
        if new_trainer.employment_status != "Active":
            raise ValidationError({"trainer":"Trainer is not active."})

        history = GeneralTrainingService._create_change_history(
            assignment=current,
            new_trainer=new_trainer,
            reason=reason,
            rating=rating,
            comments=comments,
            changed_by=changed_by,
        )

        GeneralTrainingService.close_assignment(
            assignment=current,
            status=GeneralTrainerAssignment.AssignmentStatus.TRANSFERRED,
        )

        new_assignment = GeneralTrainingService.assign_trainer(
            member=member,
            membership=current.membership,
            trainer=new_trainer,
            assigned_by=changed_by,
            assignment_mode=current.assignment_mode,
            notes=f"Transferred from {current.trainer}",
        )

        return {"history": history, "assignment": new_assignment}

    @staticmethod
    @transaction.atomic
    def auto_assign_trainer(*, member, membership, assigned_by=None):
        from trainers.models import Trainer

        trainer = Trainer.objects.filter(
            employment_status="Active",
            available_for_pi=True,
        ).order_by("active_clients","id").first()

        if trainer is None:
            raise ValidationError({"trainer":"No active trainer is available for assignment."})

        return GeneralTrainingService.assign_trainer(
            member=member,
            membership=membership,
            trainer=trainer,
            assigned_by=assigned_by,
            assignment_mode=GeneralTrainerAssignment.AssignmentMode.AUTO,
            notes="Auto assigned by FitForge.",
        )