from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def fitforge_exception_handler(exc, context):
    """
    Global exception handler for FitForge.
    Returns a consistent error response format.
    """

    response = exception_handler(exc, context)

    if response is not None:
        message = "Request failed"

        if response.status_code == status.HTTP_400_BAD_REQUEST:
            message = "Validation failed"

        elif response.status_code == status.HTTP_401_UNAUTHORIZED:
            message = "Authentication required"

        elif response.status_code == status.HTTP_403_FORBIDDEN:
            message = "Permission denied"

        elif response.status_code == status.HTTP_404_NOT_FOUND:
            message = "Resource not found"

        elif response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED:
            message = "Method not allowed"

        response.data = {
            "success": False,
            "message": message,
            "errors": response.data,
        }

    return response