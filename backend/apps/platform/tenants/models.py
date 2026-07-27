from django.db import models

from apps.platform.common.models import BaseModel


class Tenant(BaseModel):
    """
    Represents a subscriber organization/resort.
    """

    name = models.CharField(max_length=200, unique=True, db_index=True,)

    slug = models.SlugField(max_length=200, unique=True,)

    legal_name = models.CharField(max_length=255,blank=True,    )

    email = models.EmailField(blank=True, )

    phone = models.CharField(max_length=20,blank=True,)

    is_active = models.BooleanField(default=True, db_index=True,)

    class Meta:
        db_table = "tenants"
        verbose_name = "Tenant"
        verbose_name_plural = "Tenants"
        ordering = ["name"]

    def __str__(self):
        return self.name