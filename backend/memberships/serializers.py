from rest_framework import serializers

from .models import (
    MembershipPlan,
    MemberMembership,
)


class MembershipPlanSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = MembershipPlan
        fields = "__all__"


class MemberMembershipSerializer(
    serializers.ModelSerializer
):
    member_name = serializers.SerializerMethodField()

    plan_name = serializers.SerializerMethodField()

    remaining_days = serializers.ReadOnlyField()

    class Meta:
        model = MemberMembership

        fields = [
            "id",
            "member",
            "member_name",
            "plan",
            "plan_name",
            "start_date",
            "end_date",
            "status",
            "amount_paid",
            "payment_reference",
            "remaining_days",
            "created_at",
            "updated_at",
        ]

    def get_member_name(
        self,
        obj,
    ):
        return (
            f"{obj.member.first_name} "
            f"{obj.member.last_name}"
        )

    def get_plan_name(
        self,
        obj,
    ):
        return obj.plan.name

    def validate(self, attrs):
        """
        Prevent a member from having more than one
        Active membership at a time.
        """

        member = attrs.get(
            "member",
            getattr(self.instance, "member", None)
            if self.instance else None,
        )

        status = attrs.get(
            "status",
            getattr(self.instance, "status", None)
            if self.instance else None,
        )

        if member and status == "Active":

            active_memberships = (
                MemberMembership.objects
                .filter(
                    member=member,
                    status="Active",
                )
            )

            # Exclude current record during update
            if self.instance:
                active_memberships = (
                    active_memberships.exclude(
                        id=self.instance.id
                    )
                )

            if active_memberships.exists():
                raise serializers.ValidationError(
                    {
                        "member": (
                            "Member already has an active membership. "
                            "Please expire, renew, or upgrade the existing membership first."
                        )
                    }
                )

        return attrs