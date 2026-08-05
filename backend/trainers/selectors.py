from .models import Trainer


class TrainerSelector:
    @staticmethod
    def get_by_id(trainer_id):
        return Trainer.objects.filter(id=trainer_id).first()

    @staticmethod
    def get_by_phone(phone):
        return Trainer.objects.filter(phone=phone).first()

    @staticmethod
    def get_by_email(email):
        if not email:
            return None
        return Trainer.objects.filter(email=email).first()

    @staticmethod
    def list_active_trainers():
        return Trainer.objects.filter(
            employment_status="Active"
        ).order_by("trainer_code")

    @staticmethod
    def list_available_pt_trainers():
        return Trainer.objects.filter(
            employment_status="Active",
            available_for_pt=True,
        ).order_by("trainer_code")