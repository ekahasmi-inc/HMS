from django.db import models

from apps.platform.common.models import BaseModel
from apps.platform.tenants.models import Tenant


class Website(BaseModel):
    """
    Root website for a tenant.
    """
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        PUBLISHED = "PUBLISHED", "Published"
        MAINTENANCE = "MAINTENANCE", "Maintenance"

    tenant = models.OneToOneField(Tenant, on_delete=models.CASCADE, related_name="website",)
    name = models.CharField(max_length=200,)
    title = models.CharField(max_length=255, blank=True,)
    tagline = models.CharField(max_length=255, blank=True,)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT, db_index=True,)
    homepage = models.CharField(max_length=255, default="/", help_text="Homepage route",)
    is_active = models.BooleanField(default=True, db_index=True,)

    class Meta:
        db_table = "websites"
        ordering = ["name"]

    def __str__(self):
        return self.name