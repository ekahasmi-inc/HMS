from django.db import models

from apps.platform.common.models import BaseModel
from apps.platform.tenants.models import Tenant


class MediaFolder(BaseModel):
    """
    Logical folder used to organize digital assets.
    """
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="media_folders",)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name="children",)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    description = models.TextField(blank=True)
    display_order = models.PositiveIntegerField(default=0)
    is_system = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["display_order", "name"]

        constraints = [
            models.UniqueConstraint(
                fields=["tenant", "parent", "slug"],
                name="uq_mediafolder_tenant_parent_slug",
            )
        ]

    def __str__(self):
        return self.name
