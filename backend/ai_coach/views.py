from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
)

from roles.permissions import RolePermission

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


# ==========================================================
# RESPONSE SCHEMAS
# ==========================================================


class AICoachWorkoutDaySerializer(serializers.Serializer):
    day = serializers.IntegerField()
    focus = serializers.CharField()
    exercises = serializers.ListField(
        child=serializers.CharField(),
        required=False,
    )
    cardio = serializers.CharField(
        required=False,
    )


class WorkoutResponseSerializer(serializers.Serializer):
    goal = serializers.CharField()
    split = serializers.CharField(
        required=False,
    )
    days = AICoachWorkoutDaySerializer(
        many=True,
        required=False,
    )
    message = serializers.CharField(
        required=False,
    )
    generated_at = serializers.CharField()


class NutritionResponseSerializer(serializers.Serializer):
    goal = serializers.CharField()
    calories = serializers.FloatField()
    protein = serializers.IntegerField()
    carbs = serializers.IntegerField()
    fats = serializers.FloatField()


class PostureAssessmentResponseSerializer(
    serializers.Serializer
):
    issues = serializers.ListField(
        child=serializers.CharField()
    )
    corrective_exercises = serializers.ListField(
        child=serializers.CharField()
    )


# ==========================================================
# GENERATE WORKOUT
# ==========================================================


class GenerateWorkoutView(APIView):

    permission_classes = [RolePermission]

    permission_map = {
        "list": "ai_coach.use",
        "retrieve": "ai_coach.use",
        "create": "ai_coach.use",
        "update": "ai_coach.use",
        "partial_update": "ai_coach.use",
        "destroy": "ai_coach.use",
    }

    @extend_schema(
        request=WorkoutRequestSerializer,
        responses={
            200: WorkoutResponseSerializer,
            400: OpenApiResponse(
                description="Invalid workout request."
            ),
        },
        tags=["AI Coach"],
        operation_id="ai_coach_generate_workout",
    )
    def post(self, request):

        serializer = WorkoutRequestSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        result = WorkoutGeneratorService.generate(
            goal=serializer.validated_data["goal"],
            experience=serializer.validated_data["experience"],
            days_per_week=serializer.validated_data[
                "days_per_week"
            ],
        )

        return Response(result)


# ==========================================================
# GENERATE NUTRITION
# ==========================================================


class GenerateNutritionView(APIView):

    permission_classes = [RolePermission]

    permission_map = {
        "list": "ai_coach.use",
        "retrieve": "ai_coach.use",
        "create": "ai_coach.use",
        "update": "ai_coach.use",
        "partial_update": "ai_coach.use",
        "destroy": "ai_coach.use",
    }

    @extend_schema(
        request=NutritionRequestSerializer,
        responses={
            200: NutritionResponseSerializer,
            400: OpenApiResponse(
                description="Invalid nutrition request."
            ),
        },
        tags=["AI Coach"],
        operation_id="ai_coach_generate_nutrition",
    )
    def post(self, request):

        serializer = NutritionRequestSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        result = NutritionGeneratorService.generate(
            weight=serializer.validated_data["weight"],
            height=serializer.validated_data["height"],
            age=serializer.validated_data["age"],
            goal=serializer.validated_data["goal"],
        )

        return Response(result)


# ==========================================================
# POSTURE ASSESSMENT
# ==========================================================


class PostureAssessmentView(APIView):

    permission_classes = [RolePermission]

    permission_map = {
        "list": "ai_coach.use",
        "retrieve": "ai_coach.use",
        "create": "ai_coach.use",
        "update": "ai_coach.use",
        "partial_update": "ai_coach.use",
        "destroy": "ai_coach.use",
    }

    @extend_schema(
        request=PostureAssessmentSerializer,
        responses={
            200: PostureAssessmentResponseSerializer,
            400: OpenApiResponse(
                description="Invalid posture assessment request."
            ),
        },
        tags=["AI Coach"],
        operation_id="ai_coach_posture_assessment",
    )
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