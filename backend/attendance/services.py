from django.utils import timezone

from memberships.models import MemberMembership
from .models import Attendance


class AttendanceService:
    """
    Handles all attendance-related business logic.
    """

    @staticmethod
    def get_active_membership(member):
        """
        Returns the member's active membership if valid.
        """

        today = timezone.now().date()

        return (
            MemberMembership.objects.filter(
                member=member,
                status="Active",
                start_date__lte=today,
                end_date__gte=today,
            )
            .select_related("plan")
            .first()
        )

    @staticmethod
    def get_today_attendance(member):
        """
        Returns today's attendance record if one exists.
        """

        today = timezone.now().date()

        return Attendance.objects.filter(
            member=member,
            attendance_date=today,
        ).first()

    @staticmethod
    def check_in(
        member,
        branch,
        trainer=None,
        checkin_method="Reception",
        device_id=""
    ):
        """
        Performs member check-in after validating membership
        and preventing duplicate attendance.
        """

        membership = AttendanceService.get_active_membership(member)

        if not membership:
            return {
                "success": False,
                "message": "Member does not have an active membership."
            }

        existing = AttendanceService.get_today_attendance(member)

        if existing:
            return {
                "success": False,
                "message": "Member has already checked in today."
            }

        now = timezone.now()

        attendance = Attendance.objects.create(
            member=member,
            trainer=trainer,
            branch=branch,
            attendance_date=now.date(),
            check_in=now,
            status="Present",
            checkin_method=checkin_method,
            device_id=device_id,
        )

        return {
            "success": True,
            "message": "Check-in successful.",
            "attendance": attendance,
        }

    @staticmethod
    def check_out(member):
        """
        Performs member check-out.
        """

        attendance = AttendanceService.get_today_attendance(member)

        if not attendance:
            return {
                "success": False,
                "message": "No check-in found for today."
            }

        if attendance.check_out:
            return {
                "success": False,
                "message": "Member has already checked out."
            }

        attendance.check_out = timezone.now()
        attendance.save(update_fields=["check_out", "updated_at"])

        return {
            "success": True,
            "message": "Check-out successful.",
            "attendance": attendance,
            "duration": attendance.workout_duration,
        }