from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import PostureAssessment

from .serializers import (
    WorkoutRequestSerializer,
    NutritionRequestSerializer,
    PostureAssessmentSerializer,
)

from .services import (
    WorkoutGeneratorService,
    NutritionGeneratorService,
    PostureAssessmentService,
)


class GenerateWorkoutView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = WorkoutRequestSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        result = WorkoutGeneratorService.generate(
            goal=serializer.validated_data["goal"],
            experience=serializer.validated_data["experience"],
            days_per_week=serializer.validated_data["days_per_week"],
        )

        return Response(result)


class GenerateNutritionView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = NutritionRequestSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        result = NutritionGeneratorService.generate(
            weight=serializer.validated_data["weight"],
            height=serializer.validated_data["height"],
            age=serializer.validated_data["age"],
            goal=serializer.validated_data["goal"],
        )

        return Response(result)


class PostureAssessmentView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = PostureAssessmentSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        assessment = serializer.save()

        result = PostureAssessmentService.analyze()

        assessment.findings = result

        assessment.corrective_plan = result

        assessment.posture_score = 75

        assessment.save()

        return Response(result)