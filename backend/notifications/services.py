from .models import Notification


class NotificationService:

    @staticmethod
    def create_notification(
        member,
        notification_type,
        title,
        message
    ):
        return Notification.objects.create(
            member=member,
            notification_type=notification_type,
            title=title,
            message=message,
        )