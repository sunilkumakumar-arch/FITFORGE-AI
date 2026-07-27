from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils import timezone

from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

from employees.models import Employee


class AuthenticationService:
    """
    Enterprise authentication service.
    """

    @staticmethod
    def authenticate_user(employee_code, password):
        """
        Authenticate a user using employee code and password.
        """

        user = authenticate(
            username=employee_code,
            password=password,
        )

        if user is None:
            raise AuthenticationFailed(
                "Invalid employee code or password."
            )

        if not user.is_active:
            raise AuthenticationFailed(
                "Your account has been disabled."
            )

        try:
            employee = Employee.objects.select_related(
                "user",
                "user__profile",
            ).get(user=user)

        except Employee.DoesNotExist:
            raise AuthenticationFailed(
                "Employee record not found."
            )

        profile = user.profile

        tokens = AuthenticationService.generate_tokens(user)

        session = AuthenticationService.build_session(
            user,
            employee,
            profile,
        )

        return {
            "tokens": tokens,
            "session": session,
        }

    @staticmethod
    def generate_tokens(user):
        """

        
        Generate JWT access and refresh tokens.
        """

        refresh = RefreshToken.for_user(user)

        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }

    @staticmethod
    def build_session(user, employee, profile):
        """
        Build the authenticated user session returned to the client.
        """

        role = employee.role

        return {
            "user": {
                "id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "full_name": f"{user.first_name} {user.last_name}".strip(),
                "email": user.email,
            },
            "employee": {
                "id": employee.id,
                "employee_code": employee.employee_code,
                "employment_type": employee.employment_type,
                "employee_classification": employee.employee_classification,
                "employment_status": employee.employment_status,
            },
            "organization": {
                "id": employee.organization.id if employee.organization else None,
                "name": employee.organization.name if employee.organization else None,
            },
            "branch": {
                "id": employee.branch.id if employee.branch else None,
                "name": employee.branch.name if employee.branch else None,
            },
            "department": {
                "id": employee.department.id if employee.department else None,
                "name": employee.department.name if employee.department else None,
            },
            "designation": {
                "id": employee.designation.id if employee.designation else None,
                "name": employee.designation.name if employee.designation else None,
            },
            "role": {
                "id": role.id if role else None,
                "code": role.code if role else None,
                "name": role.name if role else None,
            },
            "profile": {
                "must_change_password": profile.must_change_password,
                "account_locked": profile.account_locked,
                "language": profile.language,
                "timezone": profile.timezone,
                "profile_photo": (
                    profile.profile_photo.url
                    if profile.profile_photo
                    else None
                ),
            },
        }

    @staticmethod
    def login(employee_code, password):
        """
        Complete login workflow.
        """

        auth_result = AuthenticationService.authenticate_user(
            employee_code,
            password,
        )

        return {
            "message": "Login successful.",
            "tokens": auth_result["tokens"],
            "session": auth_result["session"],
        }

 
    
    @staticmethod
    def change_password(
        user,
        current_password,
        new_password,
    ):
        """
        Change employee password.
        """
    

        

        if not user.check_password(current_password):
            raise AuthenticationFailed(
                "Current password is incorrect."
            )

        try:
            validate_password(new_password, user)
        except ValidationError as exc:
            raise AuthenticationFailed(exc.messages)

        user.set_password(new_password)
        user.save()

        profile = user.profile
        profile.must_change_password = False
        profile.last_password_change = timezone.now()
        profile.save()

        return {
            "message": "Password changed successfully."
        }