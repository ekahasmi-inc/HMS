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