from django.shortcuts import get_object_or_404

from .models import MemberHub


class MemberHubSelector:

    @staticmethod
    def get_by_member(member):
        return get_object_or_404(
            MemberHub.objects.select_related("member"),
            member=member,
        )

    @staticmethod
    def get_by_public_member_id(public_member_id):
        return get_object_or_404(
            MemberHub.objects.select_related("member"),
            public_member_id=public_member_id,
        )

    @staticmethod
    def get_by_member_code(member_code):
        return get_object_or_404(
            MemberHub.objects.select_related("member"),
            member__member_code=member_code,
        )

    @staticmethod
    def get_by_qr_token(qr_token):
        return get_object_or_404(
            MemberHub.objects.select_related("member"),
            qr_token=qr_token,
        )

    @staticmethod
    def get_queryset():
        return (
            MemberHub.objects
            .select_related("member")
            .all()
        )