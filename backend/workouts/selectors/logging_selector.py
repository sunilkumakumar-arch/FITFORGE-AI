from workouts.models import (
    WorkoutLog,
)


class WorkoutLoggingSelector:

    @staticmethod
    def get_member_logs(member):

        return (
            WorkoutLog.objects
            .select_related(
                "member_workout",
            )
            .prefetch_related(
                "exercise_logs",
            )
            .filter(
                member_workout__member=member,
            )
            .order_by("-workout_date")
        )

    @staticmethod
    def get_workout_log(log_id):

        return (
            WorkoutLog.objects
            .select_related(
                "member_workout",
            )
            .prefetch_related(
                "exercise_logs",
            )
            .get(
                id=log_id,
            )
        )