from .models import AuditLog


class AuditService:
    """
    Centralized audit logging service.
    """

    @staticmethod
    def log(
        user,
        action,
        module,
        object_id=None,
        object_name="",
        description="",
    ):
        AuditLog.objects.create(
            user=user,
            action=action,
            module=module,
            object_id=str(object_id),
            object_name=object_name,
            description=description,
        )