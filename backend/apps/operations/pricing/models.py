from apps.platform.common.models import TimeStampedModel
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.operations.booking.models import Property, RoomType,Room
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


class Season(TimeStampedModel):
    """
    Defines reusable seasonal periods used by pricing engine.
    Does not store prices.
    """
    class SeasonType(models.TextChoices):

        PEAK = "peak", "Peak Season"
        OFF = "off", "Off Season"
        HOLIDAY = "holiday", "Holiday Season"
        FESTIVE = "festive", "Festive Season"
        MONSOON = "monsoon", "Monsoon Season"
        WEEKEND = "weekend", "Weekend Season"
        CUSTOM = "custom", "Custom Season"

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="seasons",)
    name = models.CharField(max_length=200,)
    slug = models.SlugField(max_length=200,)
    description = models.TextField(blank=True,)
    season_type = models.CharField(max_length=30, choices=SeasonType.choices, default=SeasonType.CUSTOM,)
    start_date = models.DateField()
    end_date = models.DateField()
    priority = models.PositiveIntegerField(default=100, help_text="Lower value has higher priority.",)
    color_code = models.CharField(max_length=20, blank=True, help_text="UI calendar color reference.",)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE,)
    recurring = models.BooleanField(default=False, help_text="Repeat every year.",)
    applicable_months = models.JSONField(default=list, blank=True,)
    conditions = models.JSONField(default=dict, blank=True,)
    metadata = models.JSONField(default=dict, blank=True,)

    class Meta:
        ordering = ["priority","start_date",]
        constraints = [
            models.UniqueConstraint(
                fields=["property", "slug",],
                name="uq_season_property_slug",
            ),
            models.UniqueConstraint(
                fields=["property","name",],
                name="uq_season_property_name",
            ),
        ]
        indexes = [
            models.Index(
                fields=["property","status",],
                name="idx_season_property_status",
            ),
            models.Index(
                fields=["property", "start_date", "end_date",],
                name="idx_season_date_range",
            ),
            models.Index(
                fields=["season_type",],
                name="idx_season_type",
            ),
        ]

    def __str__(self):
        return f"{self.property.name} - {self.name}"



class PriceCalendar(TimeStampedModel):
    """
    Stores calculated daily selling prices.

    Prices are generated by PricingService.
    This model stores the result only.
    """
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="price_calendar",)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name="price_calendar",)
    rate_plan = models.ForeignKey(RatePlan, on_delete=models.CASCADE, related_name="price_calendar",)
    season = models.ForeignKey(Season, on_delete=models.SET_NULL, null=True, blank=True, related_name="price_calendar",)
    date = models.DateField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Original rate before adjustments",)
    adjustment_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0,)
    final_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Final sell price",)
    currency = models.CharField(max_length=10, default="INR",)
    minimum_stay = models.PositiveIntegerField(default=1,)
    maximum_stay = models.PositiveIntegerField(null=True, blank=True,)
    available_inventory = models.PositiveIntegerField(default=0,)
    occupancy_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0,)
    demand_score = models.DecimalField(max_digits=5, decimal_places=2, default=0,)
    channel = models.CharField(max_length=50, default="direct",)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE,)
    calculation_metadata = models.JSONField(default=dict, blank=True,)
    metadata = models.JSONField(default=dict,blank=True,)

    class Meta:
        ordering = ["date",]

        constraints = [
            models.UniqueConstraint(
                fields=["room_type", "rate_plan", "date", "channel",],
                name="uq_PC_room_rate_dt_channel",
            ),
        ]
        indexes = [
            models.Index(
                fields=["property", "date",],
                name="idx_PC_property_date",
            ),
            models.Index(
                fields=["room_type", "date",],
                name="idx_PC_room_date",
            ),
            models.Index(
                fields=["rate_plan", "date",],
                name="idx_PC_rate_date",
            ),
        ]
        
    def __str__(self):
        return (
            f"{self.room_type.name} "
            f"{self.date} "
            f"{self.final_price}"
        )


class DerivedRate(TimeStampedModel):
    """
    Defines inherited pricing relationships.

    Example:
    OTA rate = Base Rate + 20%
    Member rate = Base Rate - 15%
    """
    class AdjustmentType(models.TextChoices):
        PERCENTAGE = "percentage", "Percentage"
        FIXED = "fixed", "Fixed Amount"

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="derived_rates",)
    parent_rate_plan = models.ForeignKey(RatePlan, on_delete=models.CASCADE, related_name="derived_rates",)
    name = models.CharField(max_length=200,)
    slug = models.SlugField(max_length=200,)
    description = models.TextField(blank=True,)
    adjustment_type = models.CharField(max_length=30, choices=AdjustmentType.choices, default=AdjustmentType.PERCENTAGE,)
    adjustment_value = models.DecimalField(max_digits=8, decimal_places=2, help_text="Positive = markup, Negative = discount",)
    channel = models.CharField(max_length=50, blank=True, help_text="Example: OTA, Direct, Mobile",)
    customer_segment = models.CharField(max_length=100, blank=True, help_text="Example: Corporate, Member",)
    priority = models.PositiveIntegerField(default=100,)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE,)
    conditions = models.JSONField(default=dict, blank=True,)
    metadata = models.JSONField(default=dict, blank=True,)

    class Meta:
        ordering = ["priority", "name",]

        constraints = [
            models.UniqueConstraint(
                fields=["property", "slug",],
                name="uq_derived_rate_prop_slug",
            ),
            models.UniqueConstraint(
                fields=["parent_rate_plan", "name",],
                name="uq_derived_rate_plan_name",
            ),
        ]

        indexes = [
            models.Index(
                fields=["property", "status",],
                name="idx_derived_rate_prop_status",
            ),
            models.Index(
                fields=["parent_rate_plan",],
                name="idx_derived_rate_parent_plan",
            ),
            models.Index(
                fields=["channel",],
                name="idx_derived_rate_channel",
            ),
        ]


    def __str__(self):
        return (
            f"{self.parent_rate_plan.name} "
            f"→ {self.name}"
        )