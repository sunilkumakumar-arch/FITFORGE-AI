import json
from io import BytesIO

import qrcode

from django.core.files.base import ContentFile


class QRService:
    """
    Handles QR payload generation and QR image creation.
    """

    @staticmethod
    def generate_payload(member_hub):
        """
        Returns the JSON payload embedded in the QR code.
        """

        payload = {
            "type": "member_card",
            "token": str(member_hub.qr_token),
            "version": member_hub.card_version,
        }

        return json.dumps(payload)

    @classmethod
    def generate_qr_image(cls, member_hub):
        """
        Generates a QR image and returns it as a Django ContentFile.
        """

        payload = cls.generate_payload(member_hub)

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4,
        )

        qr.add_data(payload)
        qr.make(fit=True)

        image = qr.make_image(
            fill_color="black",
            back_color="white",
        )

        buffer = BytesIO()
        image.save(buffer, format="PNG")

        filename = (
            f"{member_hub.public_member_id}.png"
        )

        return filename, ContentFile(buffer.getvalue())

    @classmethod
    def save_qr_image(cls, member_hub):
        """
        Generates and stores the QR image.
        """

        filename, image = cls.generate_qr_image(member_hub)

        member_hub.qr_code.save(
            filename,
            image,
            save=True,
        )

        return member_hub

    @classmethod
    def regenerate_qr(cls, member_hub):
        """
        Deletes the old QR and creates a new one.
        """

        if member_hub.qr_code:
            member_hub.qr_code.delete(save=False)

        return cls.save_qr_image(member_hub)