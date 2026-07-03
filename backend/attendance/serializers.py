from rest_framework import serializers

from .models import Attendance


class AttendanceSerializer(
    serializers.ModelSerializer
):

    member_name = serializers.SerializerMethodField()

    trainer_name = serializers.SerializerMethodField()

    workout_duration = serializers.ReadOnlyField()

    class Meta:
        model = Attendance

        fields = [
            "id",
            "member",
            "member_name",
            "trainer",
            "trainer_name",
            "branch",
            "attendance_date",
            "check_in",
            "check_out",
            "status",
            "checkin_method",
            "device_id",
            "notes",
            "workout_duration",
            "created_at",
            "updated_at",
        ]

    def get_member_name(
        self,
        obj
    ):
        return (
            f"{obj.member.first_name} "
            f"{obj.member.last_name}"
        )

    def get_trainer_name(
        self,
        obj
    ):
        if obj.trainer:
            return (
                f"{obj.trainer.first_name} "
                f"{obj.trainer.last_name}"
            )

        return None