from django.db import transaction

from trainers.models import Trainer


class TrainerStatisticsService:
    """
    Shared service responsible for maintaining trainer statistics.
    """

    @staticmethod
    @transaction.atomic
    def increment_active_clients(trainer: Trainer):
        trainer.active_clients += 1
        trainer.save(update_fields=["active_clients"])

    @staticmethod
    @transaction.atomic
    def decrement_active_clients(trainer: Trainer):
        if trainer.active_clients > 0:
            trainer.active_clients -= 1
            trainer.save(update_fields=["active_clients"])

    @staticmethod
    @transaction.atomic
    def increment_total_clients(trainer: Trainer):
        trainer.total_clients_trained += 1
        trainer.save(update_fields=["total_clients_trained"])

    @staticmethod
    @transaction.atomic
    def update_average_rating(trainer: Trainer):
        """
        Placeholder.

        In V2 this will calculate the average
        trainer rating from GT/PT feedback history.
        """
        return trainer.rating

    @staticmethod
    @transaction.atomic
    def recalculate_active_clients(trainer: Trainer):
        """
        Placeholder.

        Future implementation will derive active
        client count from GT/PT assignments.
        """
        return trainer.active_clients