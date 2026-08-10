from django.db import models
from apps.platform.common.models import TimeStampedModel
from apps.platform.tenants.models import Tenant


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



class OTAProvider(TimeStampedModel):
    """
    Master definition of an external OTA/distribution provider.
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
    )

    name = models.CharField(
        max_length=200,
        unique=True,
    )

    display_name = models.CharField(
        max_length=200,
        blank=True,
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

    api_supported = models.BooleanField(default=False)
    webhook_supported = models.BooleanField(default=False)
    reservation_sync_supported = models.BooleanField(default=False)
    availability_sync_supported = models.BooleanField(default=False)
    rate_sync_supported = models.BooleanField(default=False)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    sort_order = models.PositiveIntegerField(default=0)

    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    class Meta:
        ordering = ["sort_order", "name"]

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


class OTAAccount(TimeStampedModel):
    """
    Tenant-specific commercial/account relationship with an OTA provider.

    This model does not store authentication credentials or synchronization
    configuration. Those responsibilities belong to OTAConnection and
    OTAAuthentication.
    """

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"
        SUSPENDED = "suspended", "Suspended"
        CLOSED = "closed", "Closed"

    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name="ota_accounts",
    )

    provider = models.ForeignKey(
        OTAProvider,
        on_delete=models.PROTECT,
        related_name="accounts",
    )

    name = models.CharField(
        max_length=200,
        help_text="Internal name for this OTA account.",
    )

    account_reference = models.CharField(
        max_length=200,
        blank=True,
        help_text="External OTA account/property reference if available.",
    )

    account_email = models.EmailField(
        blank=True,
    )

    account_username = models.CharField(
        max_length=200,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    connected_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    last_synced_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    class Meta:
        ordering = ["tenant", "provider", "name"]

        constraints = [
            models.UniqueConstraint(
                fields=["tenant", "provider", "name"],
                name="uq_ota_ac_tenant_provider_name",
            ),
        ]

        indexes = [
            models.Index(
                fields=["tenant", "status"],
                name="idx_ota_acct_tenant_status",
            ),
            models.Index(
                fields=["provider", "status"],
                name="idx_ota_acct_provider_status",
            ),
            models.Index(
                fields=["tenant", "provider"],
                name="idx_ota_acct_tenant_provider",
            ),
        ]

    def __str__(self):
        return f"{self.tenant} - {self.provider.name} - {self.name}"




class OTAConnection(TimeStampedModel):
    """
    Technical connection definition between a tenant OTA account
    and the external OTA provider.

    This model stores connection configuration and operational state.
    Credentials and secrets must remain outside this model.
    """

    class ConnectionType(models.TextChoices):
        API = "api", "API"
        WEBHOOK = "webhook", "Webhook"
        API_WEBHOOK = "api_webhook", "API + Webhook"
        SFTP = "sftp", "SFTP"
        OTHER = "other", "Other"

    class Environment(models.TextChoices):
        PRODUCTION = "production", "Production"
        SANDBOX = "sandbox", "Sandbox"
        TEST = "test", "Test"

    class ConnectionStatus(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"
        CONNECTING = "connecting", "Connecting"
        ERROR = "error", "Error"
        SUSPENDED = "suspended", "Suspended"

    ota_account = models.ForeignKey(
        "OTAAccount",
        on_delete=models.CASCADE,
        related_name="connections",
    )

    name = models.CharField(
        max_length=150,
    )

    connection_type = models.CharField(
        max_length=30,
        choices=ConnectionType.choices,
        default=ConnectionType.API,
    )

    environment = models.CharField(
        max_length=30,
        choices=Environment.choices,
        default=Environment.PRODUCTION,
    )

    endpoint = models.URLField(
        max_length=500,
        blank=True,
    )

    status = models.CharField(
        max_length=30,
        choices=ConnectionStatus.choices,
        default=ConnectionStatus.INACTIVE,
    )

    sync_enabled = models.BooleanField(
        default=True,
    )

    sync_configuration = models.JSONField(
        default=dict,
        blank=True,
    )

    last_connected_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    class Meta:
        ordering = [
            "ota_account",
            "name",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "ota_account",
                    "name",
                ],
                name="uq_ota_connection_account_name",
            ),
        ]

        indexes = [
            models.Index(
                fields=[
                    "ota_account",
                    "status",
                ],
                name="idx_ota_conn_account_status",
            ),
            models.Index(
                fields=[
                    "ota_account",
                    "environment",
                ],
                name="idx_ota_conn_account_env",
            ),
            models.Index(
                fields=[
                    "status",
                ],
                name="idx_ota_conn_status",
            ),
        ]

    def __str__(self):
        return f"{self.ota_account} - {self.name}"