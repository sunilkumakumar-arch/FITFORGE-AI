from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Member
from memberships.models import MemberMembership
from trainers.models import Trainer

from .selectors import GeneralTrainingSelector
from .serializers import (
    AssignTrainerSerializer,
    AutoAssignTrainerSerializer,
    ChangeTrainerSerializer,
    GeneralTrainerAssignmentSerializer,
    GeneralTrainerChangeHistorySerializer,
)
from .services import GeneralTrainingService


class AssignTrainerAPIView(APIView):

    def post(self, request):

        serializer = AssignTrainerSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        member = get_object_or_404(
            Member,
            pk=serializer.validated_data["member_id"],
        )

        membership = get_object_or_404(
            MemberMembership,
            pk=serializer.validated_data["membership_id"],
        )

        trainer = get_object_or_404(
            Trainer,
            pk=serializer.validated_data["trainer_id"],
        )

        assignment = (
            GeneralTrainingService.assign_trainer(
                member=member,
                membership=membership,
                trainer=trainer,
                assigned_by=request.user,
                notes=serializer.validated_data.get(
                    "notes",
                    "",
                ),
            )
        )

        return Response(
            {
                "success": True,
                "message": "Trainer assigned successfully.",
                "data": GeneralTrainerAssignmentSerializer(
                    assignment
                ).data,
            },
            status=status.HTTP_201_CREATED,
        )

class AutoAssignTrainerAPIView(APIView):

    def post(self, request):

        serializer = AutoAssignTrainerSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        member = get_object_or_404(
            Member,
            pk=serializer.validated_data["member_id"],
        )

        membership = get_object_or_404(
            MemberMembership,
            pk=serializer.validated_data["membership_id"],
        )

        assignment = (
            GeneralTrainingService.auto_assign_trainer(
                member=member,
                membership=membership,
                assigned_by=request.user,
            )
        )

        return Response(
            {
                "success": True,
                "message": "Trainer auto assigned successfully.",
                "data": GeneralTrainerAssignmentSerializer(
                    assignment
                ).data,
            },
            status=status.HTTP_201_CREATED,
        )


class ChangeTrainerAPIView(APIView):

    def post(self, request):

        serializer = ChangeTrainerSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        member = get_object_or_404(
            Member,
            pk=serializer.validated_data["member_id"],
        )

        trainer = get_object_or_404(
            Trainer,
            pk=serializer.validated_data["new_trainer_id"],
        )

        result = (
            GeneralTrainingService.change_trainer(
                member=member,
                new_trainer=trainer,
                reason=serializer.validated_data["reason"],
                rating=serializer.validated_data["rating"],
                comments=serializer.validated_data.get(
                    "comments",
                    "",
                ),
                changed_by=request.user,
            )
        )

        return Response(
            {
                "success": True,
                "message": "Trainer changed successfully.",
                "data": GeneralTrainerAssignmentSerializer(
                    result["assignment"]
                ).data,
            }
        )
class MemberAssignmentAPIView(APIView):

    def get(self, request, member_id):

        member = get_object_or_404(
            Member,
            pk=member_id,
        )

        assignment = (
            GeneralTrainingSelector.get_current_assignment(
                member
            )
        )

        if not assignment:

            return Response(
                {
                    "success": False,
                    "message": "No active assignment found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            {
                "success": True,
                "data": GeneralTrainerAssignmentSerializer(
                    assignment
                ).data,
            }
        )

class TrainerHistoryAPIView(APIView):

    def get(self, request, member_id):

        member = get_object_or_404(
            Member,
            pk=member_id,
        )

        history = (
            GeneralTrainingSelector.get_change_history(
                member
            )
        )

        return Response(
            {
                "success": True,
                "data": GeneralTrainerChangeHistorySerializer(
                    history,
                    many=True,
                ).data,
            }
        )                    



