from django.db import models
from django.utils import timezone

from apps.platform.common.models import BaseModel
from apps.platform.subscriptions.models import Subscription
from apps.platform.tenants.models import Tenant


class License(BaseModel):
    """
    Software license issued to a tenant.
    """

    class LicenseType(models.TextChoices):
        TRIAL = "TRIAL", "Trial"
        SUBSCRIPTION = "SUBSCRIPTION", "Subscription"
        LIFETIME = "LIFETIME", "Lifetime"
        ENTERPRISE = "ENTERPRISE", "Enterprise"

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        ACTIVE = "ACTIVE", "Active"
        SUSPENDED = "SUSPENDED", "Suspended"
        EXPIRED = "EXPIRED", "Expired"
        REVOKED = "REVOKED", "Revoked"

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="licenses",)
    subscription = models.ForeignKey(Subscription, on_delete=models.PROTECT, related_name="licenses", null=True, blank=True,)
    license_type = models.CharField(max_length=20, choices=LicenseType.choices, default=LicenseType.SUBSCRIPTION, db_index=True,)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING, db_index=True,)
    issued_at = models.DateTimeField(default=timezone.now,)
    valid_from = models.DateField()
    valid_until = models.DateField(null=True, blank=True,)
    notes = models.TextField(blank=True,)

    class Meta:
        db_table = "licenses"
        verbose_name = "License"
        verbose_name_plural = "Licenses"
        ordering = ["-issued_at"]

    def __str__(self):
        return f"{self.tenant.name} ({self.license_type})"