from workouts.models import MemberWorkoutPlan


class AssignmentSelector:

    @staticmethod
    def get_active_plan(member):
        return (
            MemberWorkoutPlan.objects
            .select_related(
                "member",
                "trainer",
                "workout_template",
            )
            .filter(
                member=member,
                status="ACTIVE",
            )
            .first()
        )

    @staticmethod
    def get_member_plans(member):
        return (
            MemberWorkoutPlan.objects
            .select_related(
                "trainer",
                "workout_template",
            )
            .filter(
                member=member,
            )
            .order_by("-created_at")
        )

    @staticmethod
    def get_plan(plan_id):
        return (
            MemberWorkoutPlan.objects
            .select_related(
                "member",
                "trainer",
                "workout_template",
            )
            .get(
                id=plan_id,
            )
        )