from django.db import models

from apps.platform.common.models import BaseModel


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