from rest_framework.exceptions import ValidationError


def validate_membership_dates(start_date, end_date):
    if end_date <= start_date:
        raise ValidationError(
            "End date must be greater than start date."
        )


def validate_membership_amount(amount):
    if amount < 0:
        raise ValidationError(
            "Amount cannot be negative."
        )