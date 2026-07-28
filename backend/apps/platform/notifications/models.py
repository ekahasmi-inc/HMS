from django.db import models

from apps.platform.common.models import BaseModel


class NotificationTemplate(BaseModel):
    """
    Reusable notification templates.
    """
    class Channel(models.TextChoices):
        EMAIL = "EMAIL", "Email"
        SMS = "SMS", "SMS"
        WHATSAPP = "WHATSAPP", "WhatsApp"
        PUSH = "PUSH", "Push"
        IN_APP = "IN_APP", "In-App"

    name = models.CharField(max_length=150, unique=True,)
    code = models.SlugField(max_length=150, unique=True, db_index=True,)
    channel = models.CharField(max_length=20, choices=Channel.choices, db_index=True,)
    subject = models.CharField(max_length=255, blank=True,)
    body = models.TextField()
    is_active = models.BooleanField(default=True,db_index=True,)

    class Meta:
        db_table = "notification_templates"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.channel})"