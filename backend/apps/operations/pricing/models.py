from apps.platform.common.models import TimeStampedModel
from django.core.validators import MinValueValidator, MaxValueValidator
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



class RateRule(TimeStampedModel):
    """
    Reusable pricing rules evaluated by PricingService.
    This model defines pricing logic only and never stores calculated prices.
    """
    class RuleType(models.TextChoices):
        PERCENTAGE_DISCOUNT = "percentage_discount", "Percentage Discount"
        PERCENTAGE_SURCHARGE = "percentage_surcharge", "Percentage Surcharge"
        FIXED_DISCOUNT = "fixed_discount", "Fixed Discount"
        FIXED_SURCHARGE = "fixed_surcharge", "Fixed Surcharge"
        OCCUPANCY = "occupancy", "Occupancy Based"
        LENGTH_OF_STAY = "length_of_stay", "Length of Stay"
        EARLY_BIRD = "early_bird", "Early Bird"
        LAST_MINUTE = "last_minute", "Last Minute"
        CHANNEL = "channel", "Channel Specific"
        CUSTOM = "custom", "Custom"

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="rate_rules",)
    rate_plan = models.ForeignKey(RatePlan, on_delete=models.CASCADE, related_name="rules",)
    name = models.CharField(max_length=200,)
    slug = models.SlugField(max_length=200,)
    description = models.TextField(blank=True,)
    rule_type = models.CharField(max_length=40, choices=RuleType.choices,)
    adjustment_value = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)],)
    priority = models.PositiveIntegerField(default=100, help_text="Lower numbers execute first.",)
    stackable = models.BooleanField(default=True,)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE,)
    valid_from = models.DateField(null=True, blank=True,)
    valid_to = models.DateField(null=True, blank=True,)
    minimum_nights = models.PositiveIntegerField(default=1,)
    maximum_nights = models.PositiveIntegerField(null=True, blank=True,)
    minimum_occupancy = models.PositiveIntegerField(default=1,)
    maximum_occupancy = models.PositiveIntegerField(null=True, blank=True,)
    booking_window_min_days = models.PositiveIntegerField(default=0,)
    booking_window_max_days = models.PositiveIntegerField(null=True, blank=True,)
    weekdays = models.JSONField(default=list, blank=True, help_text="Applicable weekdays (0=Monday ... 6=Sunday)",)
    channels = models.JSONField(default=list, blank=True, help_text="Applicable booking channels",)
    conditions = models.JSONField(default=dict, blank=True,)
    metadata = models.JSONField(default=dict, blank=True,)

    class Meta:
        ordering = ["priority", "name",]

        constraints = [
            models.UniqueConstraint(
                fields=["rate_plan", "slug",],
                name="uq_raterule_rateplan_slug",
            ),
            models.UniqueConstraint(
                fields=["rate_plan", "name",],
                name="uq_raterule_rateplan_name",
            ),
        ]

        indexes = [
            models.Index(
                fields=["property", "status",],
                name="idx_raterule_property_status",
            ),
            models.Index(
                fields=["rate_plan", "priority",],
                name="idx_raterule_priority",
            ),
            models.Index(
                fields=["rule_type",],
                name="idx_raterule_type",
            ),
        ]

    def __str__(self):
        return f"{self.rate_plan.name} - {self.name}"