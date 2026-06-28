from rest_framework import serializers

from .models import PostureAssessment


class WorkoutRequestSerializer(serializers.Serializer):

    goal = serializers.CharField()

    experience = serializers.CharField()

    days_per_week = serializers.IntegerField()


class NutritionRequestSerializer(serializers.Serializer):

    weight = serializers.FloatField()

    height = serializers.FloatField()

    age = serializers.IntegerField()

    goal = serializers.CharField()


class PostureAssessmentSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = PostureAssessment

        fields = "__all__"