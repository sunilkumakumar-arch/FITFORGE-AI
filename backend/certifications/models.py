from django.db import models


class Certification(models.Model):
    name = models.CharField(max_length=150, unique=True)
    issuing_organization = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name