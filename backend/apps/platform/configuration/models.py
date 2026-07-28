from django.db import models
from apps.platform.subscriptions.models import Feature
from apps.platform.common.models import BaseModel
from apps.platform.tenants.models import Tenant

class ConfigurationCategory(BaseModel):
    """
    Logical grouping of configuration keys.
    """
    name = models.CharField(max_length=100, unique=True, db_index=True,)
    code = models.SlugField(max_length=100, unique=True, help_text="Stable internal identifier.",)
    description = models.TextField(blank=True,)
    display_order = models.PositiveIntegerField(default=0,)
    is_active = models.BooleanField(default=True, db_index=True,)

    class Meta:
        db_table = "configuration_categories"
        ordering = ["display_order", "name",]
        verbose_name = "Configuration Category"
        verbose_name_plural = "Configuration Categories"

    def __str__(self):
        return self.name

class ConfigurationKey(BaseModel):
    """
    Defines a configurable setting available in the platform.
    """
    class DataType(models.TextChoices):
        STRING = "STRING", "String"
        INTEGER = "INTEGER", "Integer"
        DECIMAL = "DECIMAL", "Decimal"
        BOOLEAN = "BOOLEAN", "Boolean"
        DATE = "DATE", "Date"
        TIME = "TIME", "Time"
        DATETIME = "DATETIME", "Date Time"
        JSON = "JSON", "JSON"
        EMAIL = "EMAIL", "Email"
        URL = "URL", "URL"
        COLOR = "COLOR", "Color"

    category = models.ForeignKey(ConfigurationCategory, on_delete=models.PROTECT, related_name="configuration_keys",)
    name = models.CharField(max_length=150,)
    code = models.SlugField(max_length=150, unique=True, db_index=True, help_text="Unique internal configuration identifier.",)
    description = models.TextField(blank=True,)
    data_type = models.CharField(max_length=20, choices=DataType.choices, default=DataType.STRING, db_index=True,)
    default_value = models.TextField(blank=True, help_text="Stored as text and interpreted according to data_type.",)
    validation_rules = models.JSONField(default=dict, blank=True,
        help_text=("Validation metadata such as min/max, regex, "  "allowed values, or length constraints."),)
    ui_schema = models.JSONField(default=dict, blank=True, 
        help_text=("UI rendering metadata such as widget type, " "placeholder, help text, grouping, etc."),)
    is_required = models.BooleanField(default=False,)
    is_system = models.BooleanField(default=False, help_text="System keys cannot be deleted.",)
    is_active = models.BooleanField(default=True,)
    display_order = models.PositiveIntegerField(default=0,)

    class Meta:
        db_table = "configuration_keys"
        verbose_name = "Configuration Key"
        verbose_name_plural = "Configuration Keys"
        ordering = [
            "category__display_order",
            "display_order",
            "name",
        ]

    def __str__(self):
        return f"{self.category.name} - {self.name}"

class ConfigurationValue(BaseModel):
    """
    Stores tenant-specific configuration values.
    """
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="configuration_values",)
    configuration_key = models.ForeignKey( ConfigurationKey, on_delete=models.CASCADE, related_name="values",)
    value = models.TextField( blank=True, help_text="Stored as text. Parsed according to ConfigurationKey.data_type.",)
    is_active = models.BooleanField(default=True, db_index=True,)

    class Meta:
        db_table = "configuration_values"
        verbose_name = "Configuration Value"
        verbose_name_plural = "Configuration Values"
        constraints = [models.UniqueConstraint(fields=["tenant", "configuration_key"], name="uq_configuration_value_tenant_key",)]
        ordering = ["tenant", "configuration_key",]

    def __str__(self):
        return f"{self.tenant.name} - {self.configuration_key.code}"


class FeatureFlag(BaseModel):
    """
    Runtime feature enable/disable for a tenant.
    """
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="feature_flags",)
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, related_name="feature_flags",)
    is_enabled = models.BooleanField(default=True, db_index=True,)
    rollout_percentage = models.PositiveSmallIntegerField(default=100, help_text="Reserved for gradual rollout (0–100).",)
    notes = models.TextField(blank=True,)

    class Meta:
        db_table = "feature_flags"
        verbose_name = "Feature Flag"
        verbose_name_plural = "Feature Flags"
        constraints = [models.UniqueConstraint(fields=["tenant", "feature"], name="uq_feature_flag_tenant_feature",)]
        ordering = ["tenant", "feature",]

    def __str__(self):
        return f"{self.tenant.name} - {self.feature.code}"