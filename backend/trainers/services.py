from rest_framework.exceptions import ValidationError

from .models import Trainer
from .selectors import TrainerSelector


class TrainerService:

    @staticmethod
    def create_trainer(validated_data):

        phone = validated_data.get("phone")
        email = validated_data.get("email")

        # Check duplicate phone
        if TrainerSelector.get_by_phone(phone):
            raise ValidationError(
                {
                    "phone": "Trainer with this phone number already exists."
                }
            )

        # Check duplicate email
        if email and TrainerSelector.get_by_email(email):
            raise ValidationError(
                {
                    "email": "Trainer with this email already exists."
                }
            )

        trainer = Trainer.objects.create(
            **validated_data
        )

        return trainer