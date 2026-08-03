from django.db import models

from apps.platform.common.models import BaseModel


class Property(BaseModel):
    """
    Physical property owned by a tenant.
    """

    class PropertyType(models.TextChoices):
        HOTEL = "hotel", "Hotel"
        RESORT = "resort", "Resort"
        VILLA = "villa", "Villa"
        HOMESTAY = "homestay", "Homestay"
        APARTMENT = "apartment", "Apartment"
        HOSTEL = "hostel", "Hostel"
        CAMP = "camp", "Camp"
        OTHER = "other", "Other"

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"
        CLOSED = "closed", "Closed"

    tenant = models.ForeignKey("tenants.Tenant", on_delete=models.CASCADE, related_name="properties",)
    name = models.CharField(max_length=255,)
    slug = models.SlugField(max_length=255,)
    property_type = models.CharField(max_length=30, choices=PropertyType.choices, default=PropertyType.RESORT,)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT,)
    description = models.TextField(blank=True,)
    email = models.EmailField(blank=True,)
    phone = models.CharField(max_length=30, blank=True,)
    website = models.URLField(blank=True,)
    address_line_1 = models.CharField(max_length=255, blank=True,)
    address_line_2 = models.CharField(max_length=255, blank=True,)
    city = models.CharField(max_length=100, blank=True,)
    state = models.CharField(max_length=100, blank=True,)
    country = models.CharField(max_length=100, blank=True,)
    postal_code = models.CharField(max_length=20, blank=True,)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True,)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True,)
    timezone = models.CharField(max_length=100, default="Asia/Kolkata",)
    currency = models.CharField(max_length=10, default="INR",)
    star_rating = models.PositiveSmallIntegerField(default=0,)
    metadata = models.JSONField(default=dict, blank=True,)

    class Meta:
        ordering = ["name"]

        constraints = [
            models.UniqueConstraint(
                fields=["tenant", "slug"],
                name="uq_property_tenant_slug",
            ),
            models.UniqueConstraint(
                fields=["tenant", "name"],
                name="uq_property_tenant_name",
            ),
        ]

        indexes = [
            models.Index(
                fields=["tenant", "status"],
                name="idx_property_tenant_status",
            ),
            models.Index(
                fields=["property_type"],
                name="idx_property_type",
            ),
        ]

    def __str__(self):
        return self.name