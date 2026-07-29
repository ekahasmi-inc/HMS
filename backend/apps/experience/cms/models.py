from django.db import models

from apps.platform.common.models import BaseModel
from apps.experience.website.models import Website


class Page(BaseModel):
    """
    Website page.
    """
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        PUBLISHED = "PUBLISHED", "Published"
        ARCHIVED = "ARCHIVED", "Archived"

    website = models.ForeignKey(Website, on_delete=models.CASCADE, related_name="pages",)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name="children",)
    title = models.CharField(max_length=255,)
    navigation_title = models.CharField(max_length=255, blank=True,)
    slug = models.SlugField(max_length=255,)
    path = models.CharField(max_length=500, db_index=True, help_text="Full URL path (e.g. /rooms/deluxe/)",)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT, db_index=True,)
    is_homepage = models.BooleanField(default=False, db_index=True,)
    display_order = models.PositiveIntegerField(default=0,)
    published_at = models.DateTimeField(null=True, blank=True,)

    class Meta:
        db_table = "pages"

        ordering = [
            "display_order",
            "title",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=["website", "slug"],
                name="uq_page_slug_per_website",
            ),
            models.UniqueConstraint(
                fields=["website", "path"],
                name="uq_page_path_per_website",
            ),
        ]

    def __str__(self):
        return self.title