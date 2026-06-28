from rest_framework.permissions import BasePermission
from .models import UserRole


class IsSuperAdmin(BasePermission):

    def has_permission(self, request, view):
        try:
            return (
                request.user.is_authenticated
                and request.user.role_assignment.role.name
                == "SUPER_ADMIN"
            )
        except:
            return False


class IsManager(BasePermission):

    def has_permission(self, request, view):
        try:
            return (
                request.user.is_authenticated
                and request.user.role_assignment.role.name
                == "MANAGER"
            )
        except:
            return False


class IsTrainer(BasePermission):

    def has_permission(self, request, view):
        try:
            return (
                request.user.is_authenticated
                and request.user.role_assignment.role.name
                == "TRAINER"
            )
        except:
            return False


class IsReceptionist(BasePermission):

    def has_permission(self, request, view):
        try:
            return (
                request.user.is_authenticated
                and request.user.role_assignment.role.name
                == "RECEPTIONIST"
            )
        except:
            return False


class IsMember(BasePermission):

    def has_permission(self, request, view):
        try:
            return (
                request.user.is_authenticated
                and request.user.role_assignment.role.name
                == "MEMBER"
            )
        except:
            return False
        

class IsAdminOrManager(BasePermission):

    def has_permission(self, request, view):

        try:
            role = request.user.role_assignment.role.name

            return role in [
                "SUPER_ADMIN",
                "MANAGER"
            ]

        except:
            return False     

class IsAdminOrManager(BasePermission):

    def has_permission(self, request, view):

        try:
            role = request.user.role_assignment.role.name

            return role in [
                "SUPER_ADMIN",
                "MANAGER"
            ]

        except:
            return False           