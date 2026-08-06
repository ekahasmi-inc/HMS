from apps.platform.common.models import TimeStampedModel
from apps.operations.booking.models import Property, RoomType
from django.db import models


class RatePlan(TimeStampedModel):
    """
    Defines how rooms are sold.
    Daily prices are managed separately by PriceCalendar.
    """
    class RateType(models.TextChoices):
        STANDARD = "standard", "Standard"
        CORPORATE = "corporate", "Corporate"
        PACKAGE = "package", "Package"
        OTA = "ota", "OTA"
        MEMBER = "member", "Member"
        PROMOTIONAL = "promotional", "Promotional"

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="rate_plans",)
    room_types = models.ManyToManyField(RoomType, related_name="rate_plans", blank=True,)
    name = models.CharField(max_length=200,)
    slug = models.SlugField(max_length=200,)
    code = models.CharField(max_length=30, blank=True,)
    description = models.TextField(blank=True,)
    rate_type = models.CharField(max_length=30, choices=RateType.choices, default=RateType.STANDARD,)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE,)
    is_refundable = models.BooleanField(default=True,)
    includes_breakfast = models.BooleanField(default=False,)
    minimum_advance_booking_days = models.PositiveIntegerField(default=0,)
    maximum_advance_booking_days = models.PositiveIntegerField( default=365,)
    metadata = models.JSONField(default=dict, blank=True,)

    class Meta:
        ordering = ["property", "name",]

        constraints = [
            models.UniqueConstraint(
                fields=["property", "slug",],
                name="uq_rateplan_property_slug",
            ),
            models.UniqueConstraint(
                fields=["property", "name",],
                name="uq_rateplan_property_name",
            ),
        ]

        indexes = [
            models.Index(
                fields=["property", "status",],
                name="idx_rateplan_property_status",
            ),
            models.Index(
                fields=["property", "rate_type",],
                name="idx_rateplan_property_type",
            ),
        ]

    def __str__(self):
        return f"{self.property.name} - {self.name}"