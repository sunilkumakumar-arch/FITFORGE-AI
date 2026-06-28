from django.db.models import Sum
from django.utils import timezone

from accounts.models import Member
from trainers.models import Trainer
from memberships.models import MemberMembership
from attendance.models import Attendance
from billing.models import Payment


class ReportsService:

    @staticmethod
    def get_business_report():

        today = timezone.now().date()

        total_revenue = (
            Payment.objects.filter(
                payment_status="Paid"
            ).aggregate(
                total=Sum("amount")
            )["total"] or 0
        )

        return {
            "total_members":
                Member.objects.count(),

            "active_memberships":
                MemberMembership.objects.filter(
                    status="Active"
                ).count(),

            "expired_memberships":
                MemberMembership.objects.filter(
                    status="Expired"
                ).count(),

            "total_trainers":
                Trainer.objects.count(),

            "today_attendance":
                Attendance.objects.filter(
                    attendance_date=today
                ).count(),

            "total_revenue":
                total_revenue,

            "total_payments":
                Payment.objects.count(),

            "pending_payments":
                Payment.objects.filter(
                    payment_status="Pending"
                ).count(),
        }