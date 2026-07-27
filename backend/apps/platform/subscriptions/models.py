from django.db import models
from apps.platform.common.models import BaseModel
from django.utils import timezone
from apps.platform.tenants.models import Tenant

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



class Subscription(BaseModel):
    """
    Represents a tenant's subscription to a SaaS plan.
    """

    class Status(models.TextChoices):
        TRIAL = "TRIAL", "Trial"
        ACTIVE = "ACTIVE", "Active"
        SUSPENDED = "SUSPENDED", "Suspended"
        CANCELLED = "CANCELLED", "Cancelled"
        EXPIRED = "EXPIRED", "Expired"

    class BillingStatus(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PAID = "PAID", "Paid"
        OVERDUE = "OVERDUE", "Overdue"
        FAILED = "FAILED", "Failed"

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="subscriptions",)
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, related_name="subscriptions",)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.TRIAL, db_index=True,)
    billing_status = models.CharField(max_length=20, choices=BillingStatus.choices, default=BillingStatus.PENDING, db_index=True,)
    start_date = models.DateField(default=timezone.now,)
    end_date = models.DateField()
    renewal_date = models.DateField(null=True, blank=True,)
    trial_end_date = models.DateField(null=True, blank=True,)
    auto_renew = models.BooleanField(default=True,)

    class Meta:
        db_table = "subscriptions"
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.tenant.name} - {self.plan.name}"