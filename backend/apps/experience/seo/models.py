from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from apps.platform.common.models.base import BaseModel


class SEOProfile(BaseModel):
    """
    Reusable SEO metadata that can be attached to any content object.
    """

    class IndexingStatus(models.TextChoices):
        INDEX = "index", "Index"
        NOINDEX = "noindex", "No Index"

    class FollowStatus(models.TextChoices):
        FOLLOW = "follow", "Follow"
        NOFOLLOW = "nofollow", "No Follow"

    title = models.CharField(max_length=255,)
    meta_title = models.CharField(max_length=255, blank=True,)
    meta_description = models.TextField(blank=True,)
    meta_keywords = models.TextField(blank=True, help_text="Comma separated keywords.",)
    canonical_url = models.URLField(blank=True,)
    robots_index = models.CharField(max_length=20, choices=IndexingStatus.choices, default=IndexingStatus.INDEX,)
    robots_follow = models.CharField(max_length=20, choices=FollowStatus.choices, default=FollowStatus.FOLLOW,)
    og_title = models.CharField( max_length=255, blank=True,)
    og_description = models.TextField(blank=True,)
    og_image = models.URLField(blank=True,)
    twitter_title = models.CharField(max_length=255,blank=True,)
    twitter_description = models.TextField(blank=True,)
    twitter_image = models.URLField(blank=True,)
    schema_enabled = models.BooleanField(default=True,)
    metadata = models.JSONField(default=dict,blank=True,)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,)
    object_id = models.UUIDField()
    content_object = GenericForeignKey("content_type", "object_id",)

    class Meta:
        ordering = ["title",]
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "content_type",
                    "object_id",
                ],
                name="uq_seo_profile_target",
            )
        ]

        indexes = [
            models.Index(
                fields=[
                    "content_type",
                    "object_id",
                ],
                name="idx_seo_target",
            )
        ]

    def __str__(self):
        return self.title



class MetaTemplate(BaseModel):
    """
    Dynamic SEO metadata template.
    """
    class TemplateType(models.TextChoices):
        WEBSITE = "website", "Website"
        PAGE = "page", "Page"
        ROOM = "room", "Room"
        RESTAURANT = "restaurant", "Restaurant"
        BLOG = "blog", "Blog"
        OFFER = "offer", "Offer"
        EVENT = "event", "Event"
        GENERIC = "generic", "Generic"

    tenant = models.ForeignKey("tenants.Tenant", on_delete=models.CASCADE, related_name="meta_templates",)
    name = models.CharField( max_length=150,)
    template_type = models.CharField(max_length=30, choices=TemplateType.choices, default=TemplateType.GENERIC,)
    title_template = models.CharField( max_length=255,)
    description_template = models.TextField()
    keyword_template = models.TextField(blank=True,)
    canonical_template = models.CharField(max_length=500, blank=True,)
    og_title_template = models.CharField(max_length=255, blank=True,)
    og_description_template = models.TextField(blank=True,)
    twitter_title_template = models.CharField( max_length=255,blank=True,)
    twitter_description_template = models.TextField(blank=True,)
    available_variables = models.JSONField(default=list, blank=True,)
    is_default = models.BooleanField(default=False,)
    is_active = models.BooleanField(default=True,)
    notes = models.TextField(blank=True,)

    class Meta:
        ordering = [
            "template_type",
            "name",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=["tenant", "name"],
                name="uq_meta_template_name",
            )
        ]

        indexes = [
            models.Index(
                fields=["tenant", "template_type"],
                name="idx_meta_template_type",
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.template_type})"


class Redirect(BaseModel):
    """
    Centralized URL redirect management.
    """
    class RedirectType(models.TextChoices):
        PERMANENT_301 = "301", "301 Permanent"
        FOUND_302 = "302", "302 Found"
        TEMPORARY_307 = "307", "307 Temporary"
        PERMANENT_308 = "308", "308 Permanent"

    tenant = models.ForeignKey("tenants.Tenant", on_delete=models.CASCADE, related_name="redirects",)
    source_path = models.CharField(max_length=500, help_text="Old URL path (e.g. /rooms/deluxe-room/).",)
    destination_path = models.CharField(max_length=500, help_text="New URL or absolute URL.",)
    redirect_type = models.CharField(max_length=3, choices=RedirectType.choices, default=RedirectType.PERMANENT_301,)
    is_active = models.BooleanField(default=True,)
    preserve_query_string = models.BooleanField(default=True,)
    hit_count = models.PositiveBigIntegerField(default=0, editable=False,)
    last_accessed_at = models.DateTimeField(null=True, blank=True,)
    notes = models.TextField(blank=True,)

    class Meta:
        ordering = [
            "source_path",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "tenant",
                    "source_path",
                ],
                name="uq_redirect_source",
            )
        ]

        indexes = [
            models.Index(
                fields=[
                    "tenant",
                    "source_path",
                ],
                name="idx_redirect_lookup",
            ),
            models.Index(
                fields=[
                    "is_active",
                ],
                name="idx_redirect_active",
            ),
        ]

    def __str__(self):
        return f"{self.source_path} → {self.destination_path}"


