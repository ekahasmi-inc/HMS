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

from django.conf import settings


class PageRevision(BaseModel):
    """
    Version history for a page.
    """
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        PUBLISHED = "PUBLISHED", "Published"
        ARCHIVED = "ARCHIVED", "Archived"

    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name="revisions",)
    version = models.PositiveIntegerField()
    title = models.CharField(max_length=255,)
    notes = models.TextField(blank=True,)
    content = models.JSONField(default=dict, blank=True, help_text="Serialized page content snapshot.",)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT, db_index=True,)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="page_revisions_created",)
    published_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="page_revisions_published",)
    published_at = models.DateTimeField(null=True, blank=True,)

    class Meta:
        db_table = "page_revisions"
        ordering = [
            "-version",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=["page", "version"],
                name="uq_page_revision_version",
            )
        ]

    def __str__(self):
        return f"{self.page.title} v{self.version}"


class ContentBlock(BaseModel):
    """
    Configurable content block belonging to a page.
    """

    class BlockType(models.TextChoices):
        HERO = "HERO", "Hero"
        TEXT = "TEXT", "Text"
        GALLERY = "GALLERY", "Gallery"
        IMAGE = "IMAGE", "Image"
        VIDEO = "VIDEO", "Video"
        CTA = "CTA", "Call To Action"
        FAQ = "FAQ", "FAQ"
        TESTIMONIAL = "TESTIMONIAL", "Testimonial"
        AMENITIES = "AMENITIES", "Amenities"
        ROOM_LIST = "ROOM_LIST", "Room List"
        CONTACT = "CONTACT", "Contact"
        CUSTOM = "CUSTOM", "Custom"

    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name="content_blocks",)
    block_type = models.CharField(max_length=30, choices=BlockType.choices, db_index=True,)
    identifier = models.SlugField(max_length=100, help_text="Unique block identifier within the page.",)
    title = models.CharField(max_length=255, blank=True,)
    configuration = models.JSONField(default=dict, blank=True, help_text="Block configuration and content.",)
    display_order = models.PositiveIntegerField(default=0, db_index=True,)
    is_visible = models.BooleanField(default=True, db_index=True,)

    class Meta:
        db_table = "content_blocks"
        ordering = ["display_order",]
        constraints = [
            models.UniqueConstraint(
                fields=["page", "identifier"],
                name="uq_page_content_block_identifier",
            )
        ]

    def __str__(self):
        return f"{self.page.title} - {self.identifier}"