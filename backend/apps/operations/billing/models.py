from django.conf import settings
from django.db import models

from apps.operations.booking.models import Guest, Reservation
from apps.operations.booking.models import Property
from apps.platform.common.models import TimeStampedModel


class Folio(TimeStampedModel):
    """
    Financial account for a guest stay.

    Folio stores the financial container for a reservation.
    Charges, taxes, discounts, payments, and adjustments are
    represented by separate billing models.
    """

    class FolioType(models.TextChoices):
        GUEST = "guest", "Guest Folio"
        MASTER = "master", "Master Folio"
        COMPANY = "company", "Company Folio"
        HOUSE = "house", "House Folio"
        OTHER = "other", "Other"

    class Status(models.TextChoices):
        OPEN = "open", "Open"
        PARTIALLY_PAID = "partially_paid", "Partially Paid"
        PAID = "paid", "Paid"
        CLOSED = "closed", "Closed"
        VOID = "void", "Void"

    tenant = models.ForeignKey(
        "tenants.Tenant",
        on_delete=models.CASCADE,
        related_name="folios",
    )

    property = models.ForeignKey(
        Property,
        on_delete=models.PROTECT,
        related_name="folios",
    )

    reservation = models.ForeignKey(
        Reservation,
        on_delete=models.PROTECT,
        related_name="folios",
    )

    guest = models.ForeignKey(
        Guest,
        on_delete=models.PROTECT,
        related_name="folios",
    )

    folio_number = models.CharField(
        max_length=50,
    )

    folio_type = models.CharField(
        max_length=20,
        choices=FolioType.choices,
        default=FolioType.GUEST,
    )

    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.OPEN,
    )

    currency = models.CharField(
        max_length=3,
        default="INR",
    )

    opening_balance = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
    )

    closing_balance = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
    )

    opened_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    closed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    closed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="closed_folios",
    )

    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    class Meta:
        ordering = ["-created_at",]
        constraints = [
            models.UniqueConstraint(
                fields=["tenant","folio_number",],
                name="uq_folio_tenant_number",
            ),
        ]
        indexes = [
            models.Index(
                fields=["tenant","property", "status",],
                name="idx_folio_tenant_prop_status",
            ),
            models.Index(
                fields=["reservation","status",],
                name="idx_folio_reservation_status",
            ),
            models.Index(
                fields=["guest","status",],
                name="idx_folio_guest_status",
            ),
            models.Index(
                fields=["property", "folio_type",],
                name="idx_folio_property_type",
            ),
        ]
    def __str__(self):
        return f"{self.folio_number} - {self.guest}"



class FolioItem(TimeStampedModel):
    """
    Individual billable financial line belonging to a Folio.

    FolioItem stores the financial line record only.
    Tax calculation, discount calculation, payment processing,
    posting and other business rules belong to future services.
    """

    class ItemType(models.TextChoices):
        ROOM = "room", "Room Charge"
        RESTAURANT = "restaurant", "Restaurant"
        EXTRA_BED = "extra_bed", "Extra Bed"
        MINIBAR = "minibar", "Minibar"
        ACTIVITY = "activity", "Activity"
        TRANSFER = "transfer", "Transfer"
        SERVICE = "service", "Service Fee"
        LAUNDRY = "laundry", "Laundry"
        SPA = "spa", "Spa"
        EVENT = "event", "Event"
        OTHER = "other", "Other"

    class Status(models.TextChoices):
        POSTED = "posted", "Posted"
        VOID = "void", "Void"
        PENDING = "pending", "Pending"

    tenant = models.ForeignKey(
        "tenants.Tenant",
        on_delete=models.CASCADE,
        related_name="folio_items",
    )

    folio = models.ForeignKey(
        Folio,
        on_delete=models.CASCADE,
        related_name="items",
    )

    item_type = models.CharField(
        max_length=30,
        choices=ItemType.choices,
        default=ItemType.OTHER,
    )

    description = models.CharField(
        max_length=255,
    )

    quantity = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        default=1,
    )

    unit_price = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
    )

    amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
    )

    currency = models.CharField(
        max_length=3,
        default="INR",
    )

    service_date = models.DateField(
        null=True,
        blank=True,
    )

    posted_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.POSTED,
    )

    source_type = models.CharField(
        max_length=50,
        blank=True,
    )

    source_reference = models.CharField(
        max_length=100,
        blank=True,
    )

    sort_order = models.PositiveIntegerField(
        default=0,
    )

    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    class Meta:
        ordering = [
            "service_date",
            "sort_order",
            "created_at",
        ]

        indexes = [
            models.Index(
                fields=[
                    "tenant",
                    "folio",
                ],
                name="idx_folioitem_tenant_folio",
            ),

            models.Index(
                fields=[
                    "folio",
                    "item_type",
                ],
                name="idx_folioitem_folio_type",
            ),

            models.Index(
                fields=[
                    "folio",
                    "service_date",
                ],
                name="idx_folioitem_folio_date",
            ),

            models.Index(
                fields=[
                    "tenant",
                    "status",
                ],
                name="idx_folioitem_tenant_status",
            ),
        ]

    def __str__(self):
        return f"{self.folio.folio_number} - {self.description}"



class Charge(TimeStampedModel):
    """
    Standardized charge definition used by the billing layer.

    Charge defines what can be charged.
    Actual guest-level financial postings belong to FolioItem.
    """

    class ChargeType(models.TextChoices):
        ROOM = "room", "Room Tariff"
        RESTAURANT = "restaurant", "Restaurant"
        EXTRA_BED = "extra_bed", "Extra Bed"
        MINIBAR = "minibar", "Minibar"
        LAUNDRY = "laundry", "Laundry"
        SPA = "spa", "Spa"
        TRANSFER = "transfer", "Transfer"
        SERVICE = "service", "Service Charge"
        CANCELLATION = "cancellation", "Cancellation Fee"
        EARLY_CHECKIN = "early_checkin", "Early Check-in"
        LATE_CHECKOUT = "late_checkout", "Late Checkout"
        ACTIVITY = "activity", "Activity"
        EVENT = "event", "Event"
        OTHER = "other", "Other"

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"

    tenant = models.ForeignKey(
        "tenants.Tenant",
        on_delete=models.CASCADE,
        related_name="charges",
    )

    name = models.CharField(
        max_length=200,
    )

    slug = models.SlugField(
        max_length=200,
    )

    code = models.CharField(
        max_length=50,
        blank=True,
    )

    charge_type = models.CharField(
        max_length=30,
        choices=ChargeType.choices,
        default=ChargeType.OTHER,
    )

    description = models.TextField(
        blank=True,
    )

    default_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
    )

    currency = models.CharField(
        max_length=3,
        default="INR",
    )

    unit = models.CharField(
        max_length=30,
        default="unit",
    )

    taxable = models.BooleanField(
        default=True,
    )

    active = models.BooleanField(
        default=True,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    sort_order = models.PositiveIntegerField(
        default=0,
    )

    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    class Meta:
        ordering = [
            "sort_order",
            "name",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=["tenant", "slug"],
                name="uq_charge_tenant_slug",
            ),
            models.UniqueConstraint(
                fields=["tenant", "name"],
                name="uq_charge_tenant_name",
            ),
            models.UniqueConstraint(
                fields=["tenant", "code"],
                name="uq_charge_tenant_code",
            ),
        ]

        indexes = [
            models.Index(
                fields=["tenant", "charge_type"],
                name="idx_charge_tenant_type",
            ),
            models.Index(
                fields=["tenant", "status"],
                name="idx_charge_tenant_status",
            ),
            models.Index(
                fields=["tenant", "active"],
                name="idx_charge_tenant_active",
            ),
            models.Index(
                fields=["tenant", "sort_order"],
                name="idx_charge_tenant_order",
            ),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify

            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name



class TaxLine(TimeStampedModel):
    """
    Immutable tax snapshot attached to a FolioItem.

    TaxLine stores the tax that was actually applied to a
    financial line item. Tax calculation itself belongs to
    the future BillingService.
    """
    class TaxType(models.TextChoices):
        GST = "gst", "GST"
        CGST = "cgst", "CGST"
        SGST = "sgst", "SGST"
        IGST = "igst", "IGST"
        UTGST = "utgst", "UTGST"
        CESS = "cess", "Cess"
        SERVICE_TAX = "service_tax", "Service Tax"
        OTHER = "other", "Other"

    folio_item = models.ForeignKey("FolioItem", on_delete=models.PROTECT, related_name="tax_lines",)
    tax_type = models.CharField(max_length=30, choices=TaxType.choices,)
    tax_name = models.CharField(max_length=100,)
    tax_rate = models.DecimalField(max_digits=7, decimal_places=4, default=0,)
    taxable_amount = models.DecimalField(max_digits=14, decimal_places=2,)
    tax_amount = models.DecimalField(max_digits=14, decimal_places=2,)
    currency = models.CharField(max_length=3, default="INR",)
    metadata = models.JSONField(default=dict, blank=True,)

    class Meta:
        ordering = ["tax_type", "tax_name",]

        constraints = [
            models.UniqueConstraint(
                fields=["folio_item", "tax_type", "tax_name",],
                name="uq_taxline_item_type_name",
            ),
        ]

        indexes = [
            models.Index(
                fields=["folio_item","tax_type",],
                name="idx_taxline_item_type",
            ),
            models.Index(
                fields=["tax_name",],
                name="idx_taxline_tax_name",
            ),
        ]

    def __str__(self):
        return (
            f"{self.tax_name} - "
            f"{self.tax_amount} {self.currency}"
        )


class Discount(TimeStampedModel):
    """
    Financial discount snapshot applied to a FolioItem.

    Discount stores the resulting financial adjustment.
    Calculation logic belongs to BillingService/PricingService.
    """

    class DiscountType(models.TextChoices):
        PERCENTAGE = "percentage", "Percentage"
        FIXED = "fixed", "Fixed Amount"
        EARLY_BIRD = "early_bird", "Early Bird"
        LONG_STAY = "long_stay", "Long Stay"
        CORPORATE = "corporate", "Corporate"
        MEMBER = "member", "Member"
        COUPON = "coupon", "Coupon"
        SEASONAL = "seasonal", "Seasonal"
        PROMOTIONAL = "promotional", "Promotional"
        MANUAL = "manual", "Manual"
        OTHER = "other", "Other"

    folio_item = models.ForeignKey(
        FolioItem,
        on_delete=models.CASCADE,
        related_name="discounts",
    )

    discount_type = models.CharField(
        max_length=30,
        choices=DiscountType.choices,
        default=DiscountType.MANUAL,
    )

    name = models.CharField(
        max_length=200,
    )

    description = models.TextField(
        blank=True,
    )

    base_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
    )

    discount_rate = models.DecimalField(
        max_digits=7,
        decimal_places=4,
        null=True,
        blank=True,
        help_text="Percentage discount rate, if applicable.",
    )

    discount_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
    )

    currency = models.CharField(
        max_length=3,
        default="INR",
    )

    source_type = models.CharField(
        max_length=50,
        blank=True,
    )

    source_reference = models.CharField(
        max_length=200,
        blank=True,
    )

    reason = models.TextField(
        blank=True,
    )

    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    class Meta:
        ordering = ["id"]

        indexes = [
            models.Index(
                fields=["folio_item", "discount_type"],
                name="idx_discount_item_type",
            ),
            models.Index(
                fields=["folio_item", "name"],
                name="idx_discount_item_name",
            ),
        ]

    def __str__(self):
        return (
            f"{self.name} - "
            f"{self.discount_amount} {self.currency}"
        )