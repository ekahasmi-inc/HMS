from django.db import models

from apps.platform.common.models import BaseModel


class Tenant(BaseModel):
    """
    Represents a subscriber organization/resort.
    """

    name = models.CharField(max_length=200, unique=True, db_index=True,)

    slug = models.SlugField(max_length=200, unique=True,)

    legal_name = models.CharField(max_length=255,blank=True,    )

    email = models.EmailField(blank=True, )

    phone = models.CharField(max_length=20,blank=True,)

    is_active = models.BooleanField(default=True, db_index=True,)

    class Meta:
        db_table = "tenants"
        verbose_name = "Tenant"
        verbose_name_plural = "Tenants"
        ordering = ["name"]

    def __str__(self):
        return self.name



class TenantDomain(BaseModel):
    """
    Stores all domains and subdomains associated with a tenant.
    """

    class DomainStatus(models.TextChoices):
        PENDING = "PENDING", "Pending"
        ACTIVE = "ACTIVE", "Active"
        SUSPENDED = "SUSPENDED", "Suspended"
        EXPIRED = "EXPIRED", "Expired"

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="domains",)

    domain = models.CharField(max_length=255, unique=True, db_index=True, help_text="Example: resort.sukhavasam.in or www.clientresort.com",)

    is_primary = models.BooleanField(default=False, db_index=True,)

    is_verified = models.BooleanField(default=False,)

    ssl_enabled = models.BooleanField(default=False,)

    status = models.CharField(max_length=20, choices=DomainStatus.choices, default=DomainStatus.PENDING, db_index=True,)

    class Meta:
        db_table = "tenant_domains"
        verbose_name = "Tenant Domain"
        verbose_name_plural = "Tenant Domains"
        ordering = ["tenant", "-is_primary", "domain"]

    def __str__(self):
        return self.domain