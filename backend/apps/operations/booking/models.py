from django.db import models
from apps.platform.common.models import TimeStampedModel
from apps.platform.tenants.models import Tenant
from apps.platform.common.models import BaseModel
from django.utils.text import slugify




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


class PropertyAmenity(BaseModel):
    """
    Property-level facilities and services.
    """
    class Category(models.TextChoices):
        GENERAL = "general", "General"
        DINING = "dining", "Dining"
        WELLNESS = "wellness", "Wellness"
        RECREATION = "recreation", "Recreation"
        BUSINESS = "business", "Business"
        TRANSPORT = "transport", "Transport"
        ACCESSIBILITY = "accessibility", "Accessibility"
        SAFETY = "safety", "Safety"
        OTHER = "other", "Other"

    property = models.ForeignKey("Property", on_delete=models.CASCADE, related_name="amenities",)
    name = models.CharField(max_length=150,)
    slug = models.SlugField(max_length=150,)
    category = models.CharField(max_length=30, choices=Category.choices, default=Category.GENERAL,)
    description = models.TextField(blank=True,)
    icon = models.CharField(max_length=100, blank=True, help_text="Icon name (Font Awesome, Material Icons, etc.)",)
    display_order = models.PositiveIntegerField(default=1,)
    is_featured = models.BooleanField(default=False,)
    is_active = models.BooleanField(default=True,)
    metadata = models.JSONField(default=dict, blank=True,)

    class Meta:
        ordering = ("display_order","name",)

        constraints = [
            models.UniqueConstraint(
                fields=["property","slug",],
                name="uq_property_amenity_slug",
            ),
            models.UniqueConstraint(
                fields=["property","name",],
                name="uq_property_amenity_name",
            ),
        ]

        indexes = [
            models.Index(
                fields=["property","is_active",],
                name="idx_prop_amn_active",
            ),
            models.Index(
                fields=["category",],
                name="idx_prop_amn_cat",
            ),
        ]

    def __str__(self):
        return f"{self.property.name} - {self.name}"


class Building(TimeStampedModel):
    """
    Physical building within a property.
    """
    class BuildingType(models.TextChoices):

        MAIN = "main", "Main Building"
        VILLA = "villa", "Villa"
        BLOCK = "block", "Block"
        COTTAGE = "cottage", "Cottage"
        OTHER = "other", "Other"

    class BuildingStatus(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"
        UNDER_CONSTRUCTION = "under_construction", "Under Construction"
        CLOSED = "closed", "Closed"

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="buildings",)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    code = models.CharField(max_length=30, blank=True,)
    building_type = models.CharField(max_length=30, choices=BuildingType.choices, default=BuildingType.MAIN,)
    description = models.TextField(blank=True,)
    building_number = models.CharField(max_length=50, blank=True,)
    total_floors = models.PositiveIntegerField(default=1,)
    status = models.CharField(max_length=30, choices=BuildingStatus.choices, default=BuildingStatus.ACTIVE,)
    sort_order = models.PositiveIntegerField(default=0,)
    metadata = models.JSONField(default=dict, blank=True,)

    class Meta:
        ordering = ["sort_order", "name",]

        constraints = [
            models.UniqueConstraint(
                fields=["property", "slug"],
                name="uq_building_property_slug",
            ),
            models.UniqueConstraint(
                fields=["property", "name"],
                name="uq_building_property_name",
            ),
        ]

        indexes = [
            models.Index(
                fields=["property", "status"],
                name="idx_building_property_status",
            ),
            models.Index(
                fields=["property", "sort_order"],
                name="idx_building_property_order",
            ),
        ]

    def __str__(self):
        return f"{self.property.name} - {self.name}"

from django.db import models

from apps.platform.common.models import TimeStampedModel


class Floor(TimeStampedModel):
    """
    Physical floor within a building.
    """
    class FloorType(models.TextChoices):

        BASEMENT = "basement", "Basement"
        GROUND = "ground", "Ground Floor"
        FIRST = "first", "First Floor"
        SECOND = "second", "Second Floor"
        THIRD = "third", "Third Floor"
        TERRACE = "terrace", "Terrace"
        OTHER = "other", "Other"

    class FloorStatus(models.TextChoices):

        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"
        UNDER_MAINTENANCE = "under_maintenance", "Under Maintenance"
        CLOSED = "closed", "Closed"

    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name="floors",)
    name = models.CharField(max_length=200,)
    slug = models.SlugField( max_length=200,)
    floor_number = models.IntegerField(default=0, help_text="0 = Ground Floor",)
    floor_type = models.CharField(max_length=30, choices=FloorType.choices, default=FloorType.GROUND,)
    description = models.TextField(blank=True,)
    status = models.CharField(max_length=30, choices=FloorStatus.choices, default=FloorStatus.ACTIVE,)
    sort_order = models.PositiveIntegerField(default=0,)
    metadata = models.JSONField(default=dict, blank=True,)

    class Meta:
        ordering = ["sort_order", "floor_number", "name",]

        constraints = [
            models.UniqueConstraint(
                fields=["building", "slug",],
                name="uq_floor_building_slug",
            ),

            models.UniqueConstraint(
                fields=["building", "floor_number",],
                name="uq_floor_building_number",
            ),
        ]

        indexes = [

            models.Index(
                fields=["building", "status",],
                name="idx_floor_building_status",
            ),

            models.Index(
                fields=["building", "sort_order",],
                name="idx_floor_building_order",
            ),
        ]

    def __str__(self):
        return (
            f"{self.building.name} - {self.name}"
        )

