from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from roles.permissions import RolePermission
from .selectors import (
    MemberSelector,
    MemberProfileSelector,
    EmergencyContactSelector,
    MedicalProfileSelector,
    FitnessGoalSelector,
    BodyAssessmentSelector,
)

from .services import (
    MemberService,
    MemberProfileService,
    EmergencyContactService,
    MedicalProfileService,
    FitnessGoalService,
    BodyAssessmentService,
)
from rest_framework.response import Response
from rest_framework import status

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
    queryset = Member.objects.all()   # <-- Add this back

    serializer_class = MemberSerializer
    permission_classes = [RolePermission]

    permission_map = {
        "list": "member.view",
        "retrieve": "member.view",
        "create": "member.create",
        "update": "member.update",
        "partial_update": "member.update",
        "destroy": "member.delete",
    }

    def get_queryset(self):
        return MemberSelector.get_queryset()

    def perform_create(self, serializer):
        MemberService.create_member(serializer.validated_data)

    def perform_update(self, serializer):
        MemberService.update_member(
            serializer.instance,
            serializer.validated_data,
        )

    def perform_destroy(self, instance):
        MemberService.delete_member(instance)


class MemberProfileViewSet(viewsets.ModelViewSet):
    queryset = MemberProfile.objects.all()
    serializer_class = MemberProfileSerializer
    permission_classes = [RolePermission]

    permission_map = {
        "list": "member.view",
        "retrieve": "member.view",
        "create": "member.update",
        "update": "member.update",
        "partial_update": "member.update",
        "destroy": "member.delete",
    }

    def get_queryset(self):
        return MemberProfileSelector.get_queryset()

    def perform_create(self, serializer):
        MemberProfileService.create(serializer.validated_data)

    def perform_update(self, serializer):
        MemberProfileService.update(
            serializer.instance,
            serializer.validated_data,
        )

    def perform_destroy(self, instance):
        MemberProfileService.delete(instance)


class EmergencyContactViewSet(viewsets.ModelViewSet):
    queryset = EmergencyContact.objects.all()
    serializer_class = EmergencyContactSerializer
    permission_classes = [RolePermission]

    permission_map = {
        "list": "member.view",
        "retrieve": "member.view",
        "create": "member.update",
        "update": "member.update",
        "partial_update": "member.update",
        "destroy": "member.delete",
    }

    def get_queryset(self):
        return EmergencyContactSelector.get_queryset()

    def perform_create(self, serializer):
        EmergencyContactService.create(serializer.validated_data)

    def perform_update(self, serializer):
        EmergencyContactService.update(
            serializer.instance,
            serializer.validated_data,
        )

    def perform_destroy(self, instance):
        EmergencyContactService.delete(instance)


class MedicalProfileViewSet(viewsets.ModelViewSet):
    queryset = MedicalProfile.objects.all()
    serializer_class = MedicalProfileSerializer
    permission_classes = [RolePermission]

    permission_map = {
        "list": "member.view",
        "retrieve": "member.view",
        "create": "member.update",
        "update": "member.update",
        "partial_update": "member.update",
        "destroy": "member.delete",
    }

    def get_queryset(self):
        return MedicalProfileSelector.get_queryset()

    def perform_create(self, serializer):
        MedicalProfileService.create(serializer.validated_data)

    def perform_update(self, serializer):
        MedicalProfileService.update(
            serializer.instance,
            serializer.validated_data,
        )

    def perform_destroy(self, instance):
        MedicalProfileService.delete(instance)


class FitnessGoalViewSet(viewsets.ModelViewSet):
    queryset = FitnessGoal.objects.all()
    serializer_class = FitnessGoalSerializer
    permission_classes = [RolePermission]

    permission_map = {
        "list": "member.view",
        "retrieve": "member.view",
        "create": "member.update",
        "update": "member.update",
        "partial_update": "member.update",
        "destroy": "member.delete",
    }

    def get_queryset(self):
        return FitnessGoalSelector.get_queryset()

    def perform_create(self, serializer):
        FitnessGoalService.create(serializer.validated_data)

    def perform_update(self, serializer):
        FitnessGoalService.update(
            serializer.instance,
            serializer.validated_data,
        )

    def perform_destroy(self, instance):
        FitnessGoalService.delete(instance)


class BodyAssessmentViewSet(viewsets.ModelViewSet):
    queryset = BodyAssessment.objects.all()
    serializer_class = BodyAssessmentSerializer
    permission_classes = [RolePermission]

    permission_map = {
        "list": "member.view",
        "retrieve": "member.view",
        "create": "member.update",
        "update": "member.update",
        "partial_update": "member.update",
        "destroy": "member.delete",
    }

    def get_queryset(self):
        return BodyAssessmentSelector.get_queryset()

    def perform_create(self, serializer):
        BodyAssessmentService.create(serializer.validated_data)

    def perform_update(self, serializer):
        BodyAssessmentService.update(
            serializer.instance,
            serializer.validated_data,
        )

    def perform_destroy(self, instance):
        BodyAssessmentService.delete(instance)