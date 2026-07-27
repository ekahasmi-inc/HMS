from django.db import models

from apps.platform.common.models import BaseModel


class Plan(BaseModel):
    """
    SaaS subscription plan.
    """

    class BillingCycle(models.TextChoices):
        MONTHLY = "MONTHLY", "Monthly"
        QUARTERLY = "QUARTERLY", "Quarterly"
        YEARLY = "YEARLY", "Yearly"

    name = models.CharField( max_length=100, unique=True, db_index=True,)
    code = models.SlugField(max_length=100, unique=True, help_text="Unique system identifier (e.g. starter, professional).",)
    description = models.TextField(blank=True,)
    billing_cycle = models.CharField(max_length=20, choices=BillingCycle.choices, default=BillingCycle.MONTHLY,)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0,)
    currency = models.CharField(max_length=10, default="INR",)
    trial_days = models.PositiveIntegerField(default=0,)
    max_properties = models.PositiveIntegerField(default=1,)
    max_users = models.PositiveIntegerField(default=5,)
    is_active = models.BooleanField(default=True, db_index=True,)

    class Meta:
        db_table = "subscription_plans"
        ordering = ["price"]
        verbose_name = "Subscription Plan"
        verbose_name_plural = "Subscription Plans"

    def __str__(self):
        return self.name


class Feature(BaseModel):
    """
    Master catalog of platform capabilities.

    Features are independent of plans and tenants.
    """

    class Category(models.TextChoices):
        PLATFORM = "PLATFORM", "Platform"
        WEBSITE = "WEBSITE", "Website"
        BOOKING = "BOOKING", "Booking"
        PMS = "PMS", "PMS"
        RESTAURANT = "RESTAURANT", "Restaurant"
        CRM = "CRM", "CRM"
        MARKETING = "MARKETING", "Marketing"
        ANALYTICS = "ANALYTICS", "Analytics"
        AI = "AI", "AI"
        OTA = "OTA", "OTA"
        FINANCE = "FINANCE", "Finance"

    name = models.CharField( max_length=150, unique=True, db_index=True,)
    code = models.SlugField(max_length=100, unique=True, help_text="Stable system identifier.",)
    category = models.CharField(max_length=30, choices=Category.choices, db_index=True,)
    description = models.TextField( blank=True,)
    is_active = models.BooleanField( default=True, db_index=True,)
    display_order = models.PositiveIntegerField( default=0,)

    class Meta:
        db_table = "subscription_features"
        ordering = [
            "category",
            "display_order",
            "name",
        ]
        verbose_name = "Feature"
        verbose_name_plural = "Features"

    def __str__(self):
        return self.name