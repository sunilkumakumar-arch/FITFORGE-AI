from datetime import timedelta
from django.utils import timezone


class MembershipService:

    @staticmethod
    def calculate_end_date(start_date, duration_days):
        return start_date + timedelta(days=duration_days)

    @staticmethod
    def is_active(membership):
        return (
            membership.status == "Active"
            and membership.end_date >= timezone.now().date()
        )