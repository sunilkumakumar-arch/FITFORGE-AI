from django.db import models


class BaseModel(models.Model):
    """
    Abstract base model used across the entire FitForge platform.
    """

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True