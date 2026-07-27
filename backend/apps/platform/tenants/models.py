from django.db import models

from apps.platform.common.models import BaseModel


class Tenant(BaseModel):
    """
    Represents a subscriber organization/resort.
    """

    name = models.CharField(max_length=200, unique=True, db_index=True,)
    slug = models.SlugField(max_length=200, unique=True,)
    legal_name = models.CharField(max_length=255,blank=True,)
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


class TenantBranding(BaseModel):
    """
    Branding configuration for a tenant.
    """

    tenant = models.OneToOneField(Tenant, on_delete=models.CASCADE, related_name="branding",)
    display_name = models.CharField( max_length=200,)
    tagline = models.CharField( max_length=255, blank=True,)
    logo = models.ImageField( upload_to="branding/logos/", blank=True, null=True,)
    favicon = models.ImageField( upload_to="branding/favicons/", blank=True, null=True,)
    primary_color = models.CharField( max_length=7, default="#0F766E", help_text="HEX color",)
    secondary_color = models.CharField(max_length=7, default="#FFFFFF", help_text="HEX color",)
    accent_color = models.CharField( max_length=7, default="#F59E0B", help_text="HEX color",)

    class Meta:
        db_table = "tenant_branding"
        verbose_name = "Tenant Branding"
        verbose_name_plural = "Tenant Branding"

    def __str__(self):
        return self.display_name

class TenantSettings(BaseModel):
    """
    Operational settings for a tenant.
    Does NOT store feature flags or configuration engine values.
    """

    tenant = models.OneToOneField(Tenant, on_delete=models.CASCADE, related_name="settings",)
    timezone = models.CharField(max_length=100, default="Asia/Kolkata",)
    currency = models.CharField(max_length=10, default="INR",)
    language = models.CharField( max_length=20, default="en",)
    date_format = models.CharField( max_length=30, default="DD/MM/YYYY",)
    time_format = models.CharField(max_length=10, default="24H", help_text="12H or 24H",)
    country = models.CharField(max_length=100,  blank=True,)
    state = models.CharField(max_length=100, blank=True,)
    city = models.CharField(max_length=100, blank=True,)
    address = models.TextField(blank=True,)
    postal_code = models.CharField(max_length=20, blank=True,)
    gst_number = models.CharField(max_length=30, blank=True,)
    contact_email = models.EmailField( blank=True,)
    contact_phone = models.CharField( max_length=20, blank=True,)
    check_in_time = models.TimeField( null=True, blank=True,)
    check_out_time = models.TimeField(null=True, blank=True,)

    class Meta:
        db_table = "tenant_settings"
        verbose_name = "Tenant Settings"
        verbose_name_plural = "Tenant Settings"

    def __str__(self):
        return f"{self.tenant.name} Settings"