from django.utils import timezone

from memberships.models import MemberMembership

from .models import MemberPTPackage


class PTPackageSelector:

    @staticmethod
    def get_active_membership(member):
        return (
            MemberMembership.objects.filter(
                member=member,
                status="Active",
            )
            .order_by("-end_date")
            .first()
        )

    @staticmethod
    def get_active_pt_package(member):
        return (
            MemberPTPackage.objects.filter(
                member=member,
                is_active=True,
            )
            .order_by("-expiry_date")
            .first()
        )

    @staticmethod
    def membership_remaining_days(membership):
        if not membership:
            return 0

        return (
            membership.end_date -
            timezone.now().date()
        ).days

    @staticmethod
    def package_remaining_days(package):
        if not package:
            return 0

        return (
            package.expiry_date -
            timezone.now().date()
        ).days

    @staticmethod
    def package_remaining_sessions(package):
        if not package:
            return 0

        return (
            package.package.total_sessions -
            package.sessions_used
        )