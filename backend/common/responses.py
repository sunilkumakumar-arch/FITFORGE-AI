from rest_framework import status
from rest_framework.response import Response


def success_response(
    data=None,
    message="Success",
    status_code=status.HTTP_200_OK,
):
    """
    Standard success response.
    """
    return Response(
        {
            "success": True,
            "message": message,
            "data": data,
        },
        status=status_code,
    )


def created_response(
    data=None,
    message="Created successfully.",
):
    """
    Standard created response.
    """
    return success_response(
        data=data,
        message=message,
        status_code=status.HTTP_201_CREATED,
    )


def error_response(
    message="Request failed.",
    errors=None,
    status_code=status.HTTP_400_BAD_REQUEST,
):
    """
    Standard error response.
    """
    return Response(
        {
            "success": False,
            "message": message,
            "errors": errors,
        },
        status=status_code,
    )