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