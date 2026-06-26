from rest_framework.permissions import BasePermission


class IsGymStaff(BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_staff