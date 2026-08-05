import json

from .selectors import MemberHubSelector


class VerificationService:
    """
    Handles QR verification for MemberHub.
    """

    @classmethod
    def verify_qr(cls, qr_payload):
        """
        Verifies a scanned QR payload and returns
        the corresponding MemberHub.
        """

        try:
            payload = json.loads(qr_payload)

        except json.JSONDecodeError:
            return {
                "valid": False,
                "message": "Invalid QR payload.",
            }

        if payload.get("type") != "member_card":
            return {
                "valid": False,
                "message": "Invalid QR type.",
            }

        token = payload.get("token")

        if not token:
            return {
                "valid": False,
                "message": "QR token missing.",
            }

        member_hub = MemberHubSelector.get_by_qr_token(token)

        if not member_hub:
            return {
                "valid": False,
                "message": "Member not found.",
            }

        return {
            "valid": True,
            "member_hub": member_hub,
        }