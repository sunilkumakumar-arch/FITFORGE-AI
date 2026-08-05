from accounts.models import Member

from member_hub.models import MemberHub

from memberships.models import MemberMembership

from attendance.models import Attendance

from trainer_assignments.models import TrainerAssignment

from pt_packages.models import MemberPTPackage
from django.db.models import Q

class ReceptionSelector:
    """
    Read-only queries for the Reception module.
    """

    @staticmethod
    def get_member(member_code):
        return (
            Member.objects
            .filter(member_code=member_code)
            .first()
        )

    @staticmethod
    def get_member_hub(member):
        return (
            MemberHub.objects
            .filter(member=member)
            .first()
        )

    @staticmethod
    def get_active_membership(member):
        return (
            MemberMembership.objects
            .filter(
                member=member,
                status="Active"
            )
            .select_related("plan")
            .first()
        )

    @staticmethod
    def get_today_attendance(member):
        return (
            Attendance.objects
            .filter(member=member)
            .order_by("-attendance_date", "-check_in")
            .first()
        )

    @staticmethod
    def get_trainer_assignment(member):
        return (
            TrainerAssignment.objects
            .filter(member=member)
            .select_related("trainer")
            .first()
        )

    @staticmethod
    def get_pt_package(member):
        return (
            MemberPTPackage.objects
            .filter(member=member)
            .first()
        )


    @staticmethod
    def search_members(query):
        return (
            Member.objects.filter(
                Q(member_code__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(phone__icontains=query) |
                Q(email__icontains=query)
            )
            .order_by("first_name", "last_name")[:20]
        )