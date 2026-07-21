from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    """
    Serializer for employee login.
    """

    employee_code = serializers.CharField(
        max_length=30,
        required=True,
        trim_whitespace=True,
    )

    password = serializers.CharField(
        write_only=True,
        style={"input_type": "password"},
        required=True,
    )