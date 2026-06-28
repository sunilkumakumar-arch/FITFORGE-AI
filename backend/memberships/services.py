from datetime import timedelta
from django.utils import timezone

from accounts.models import Member
from employees.models import Employee
from trainers.models import Trainer
from memberships.models import MemberMembership
from attendance.models import Attendance


class DashboardService:

    @staticmethod
    def get_summary():

        today = timezone.now().date()

        next_7_days = today + timedelta(days=7)

        return {
            "total_members":
                Member.objects.count(),

            "total_employees":
                Employee.objects.count(),

            "total_trainers":
                Trainer.objects.count(),

            "active_memberships":
                MemberMembership.objects.filter(
                    status="Active"
                ).count(),

            "expired_memberships":
                MemberMembership.objects.filter(
                    status="Expired"
                ).count(),

            "expiring_next_7_days":
                MemberMembership.objects.filter(
                    end_date__gte=today,
                    end_date__lte=next_7_days,
                    status="Active"
                ).count(),

            "today_attendance":
                Attendance.objects.filter(
                    attendance_date=today
                ).count(),

            "new_members_this_month":
                Member.objects.filter(
                    joining_date__month=today.month,
                    joining_date__year=today.year
                ).count(),
        }