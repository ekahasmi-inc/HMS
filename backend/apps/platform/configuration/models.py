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