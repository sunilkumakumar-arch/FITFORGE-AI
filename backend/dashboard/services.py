from django.utils import timezone
from django.db.models import Sum

from accounts.models import Member
from employees.models import Employee
from trainers.models import Trainer
from memberships.models import MemberMembership
from attendance.models import Attendance
from billing.models import Payment


class DashboardService:

    @staticmethod
    def get_summary():

        today = timezone.now().date()

        total_revenue = (
            Payment.objects.filter(
                payment_status="Paid"
            ).aggregate(
                total=Sum("amount")
            )["total"]
            or 0
        )

        return {
            # Members
            "total_members":
                Member.objects.count(),

            # Employees
            "total_employees":
                Employee.objects.count(),

            # Trainers
            "total_trainers":
                Trainer.objects.count(),

            # Memberships
            "active_memberships":
                MemberMembership.objects.filter(
                    status="Active"
                ).count(),

            "expired_memberships":
                MemberMembership.objects.filter(
                    status="Expired"
                ).count(),
            # Attendance
            "today_attendance":
                Attendance.objects.filter(
                    attendance_date=today
                ).count(),

            # Revenue
            "total_revenue":
                total_revenue,

            # Payments
            "total_payments":
                Payment.objects.count(),

            "pending_payments":
                Payment.objects.filter(
                    payment_status="Pending"
                ).count(),
        }