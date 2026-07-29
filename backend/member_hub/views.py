from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .selectors import MemberHubSelector
from .serializers import MemberHubSerializer


class MemberHubListView(generics.ListAPIView):
    """
    Returns all MemberHub records.
    """

    serializer_class = MemberHubSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MemberHubSelector.get_queryset()


class MemberHubDetailView(generics.RetrieveAPIView):
    """
    Returns a single MemberHub by primary key.
    """

    serializer_class = MemberHubSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MemberHubSelector.get_queryset()


class MemberHubByPublicIdView(generics.RetrieveAPIView):
    """
    Returns a MemberHub by public_member_id.
    """

    serializer_class = MemberHubSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return MemberHubSelector.get_by_public_member_id(
            self.kwargs["public_member_id"]
        )


class MemberHubByMemberCodeView(generics.RetrieveAPIView):
    """
    Returns a MemberHub by member_code.
    """

    serializer_class = MemberHubSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return MemberHubSelector.get_by_member_code(
            self.kwargs["member_code"]
        )