from django.db import models

from apps.platform.common.models import TimeStampedModel


class OTAProvider(TimeStampedModel):
    """
    Master definition of an external Online Travel Agency / distribution
    provider.

    This model represents the provider itself, not a tenant's account,
    connection, credentials, property mapping, inventory, rates, or
    reservations.
    """

    class ProviderType(models.TextChoices):
        OTA = "ota", "Online Travel Agency"
        CHANNEL_MANAGER = "channel_manager", "Channel Manager"
        DISTRIBUTION_NETWORK = "distribution_network", "Distribution Network"
        METASEARCH = "metasearch", "Metasearch"
        OTHER = "other", "Other"

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"
        DEPRECATED = "deprecated", "Deprecated"

    code = models.SlugField(
        max_length=100,
        unique=True,
        help_text="Stable internal provider code, e.g. booking-com.",
    )

    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Human-readable provider name.",
    )

    display_name = models.CharField(
        max_length=200,
        blank=True,
        help_text="Optional public/display name.",
    )

    provider_type = models.CharField(
        max_length=30,
        choices=ProviderType.choices,
        default=ProviderType.OTA,
    )

    description = models.TextField(
        blank=True,
    )

    website_url = models.URLField(
        blank=True,
    )

    api_supported = models.BooleanField(
        default=False,
    )

    webhook_supported = models.BooleanField(
        default=False,
    )

    reservation_sync_supported = models.BooleanField(
        default=False,
    )

    availability_sync_supported = models.BooleanField(
        default=False,
    )

    rate_sync_supported = models.BooleanField(
        default=False,
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
        ordering = ["sort_order","name",]

        indexes = [
            models.Index(
                fields=["status"],
                name="idx_ota_provider_status",
            ),
            models.Index(
                fields=["provider_type", "status"],
                name="idx_ota_provider_type_status",
            ),
            models.Index(
                fields=["sort_order"],
                name="idx_ota_provider_order",
            ),
        ]

    def __str__(self):
        return self.display_name or self.name