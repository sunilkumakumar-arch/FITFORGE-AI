from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import (
    Member,
    MemberProfile,
    EmergencyContact,
    MedicalProfile,
    FitnessGoal,
    BodyAssessment,
)

from .serializers import (
    MemberSerializer,
    MemberProfileSerializer,
    EmergencyContactSerializer,
    MedicalProfileSerializer,
    FitnessGoalSerializer,
    BodyAssessmentSerializer,
)


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated]


class MemberProfileViewSet(viewsets.ModelViewSet):
    queryset = MemberProfile.objects.all()
    serializer_class = MemberProfileSerializer
    permission_classes = [IsAuthenticated]


class EmergencyContactViewSet(viewsets.ModelViewSet):
    queryset = EmergencyContact.objects.all()
    serializer_class = EmergencyContactSerializer
    permission_classes = [IsAuthenticated]


class MedicalProfileViewSet(viewsets.ModelViewSet):
    queryset = MedicalProfile.objects.all()
    serializer_class = MedicalProfileSerializer
    permission_classes = [IsAuthenticated]


class FitnessGoalViewSet(viewsets.ModelViewSet):
    queryset = FitnessGoal.objects.all()
    serializer_class = FitnessGoalSerializer
    permission_classes = [IsAuthenticated]


class BodyAssessmentViewSet(viewsets.ModelViewSet):
    queryset = BodyAssessment.objects.all()
    serializer_class = BodyAssessmentSerializer
    permission_classes = [IsAuthenticated]