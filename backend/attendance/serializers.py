from rest_framework import serializers

from .models import Attendance


class AttendanceSerializer(serializers.ModelSerializer):

    workout_duration = serializers.ReadOnlyField()

    class Meta:
        model = Attendance

        fields = "__all__"