from django.apps import AppConfig


class MemberHubConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "member_hub"

    def ready(self):
        import member_hub.signals