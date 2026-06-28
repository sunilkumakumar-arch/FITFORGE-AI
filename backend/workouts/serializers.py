from rest_framework import serializers

from .models import (
    WorkoutPlan,
    WorkoutDay,
    WorkoutExercise,
    MemberWorkoutAssignment,
)


class WorkoutPlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkoutPlan
        fields = "__all__"


class WorkoutDaySerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkoutDay
        fields = "__all__"


class WorkoutExerciseSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkoutExercise
        fields = "__all__"


class MemberWorkoutAssignmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = MemberWorkoutAssignment
        fields = "__all__"