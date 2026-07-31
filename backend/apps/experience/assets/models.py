from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
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


class MediaAsset(BaseModel):

    class AssetType(models.TextChoices):
        IMAGE = "image", "Image"
        VIDEO = "video", "Video"
        AUDIO = "audio", "Audio"
        DOCUMENT = "document", "Document"
        PDF = "pdf", "PDF"
        SVG = "svg", "SVG"
        OTHER = "other", "Other"

    class StorageProvider(models.TextChoices):
        LOCAL = "local", "Local"
        S3 = "s3", "Amazon S3"
        CLOUDINARY = "cloudinary", "Cloudinary"
        AZURE = "azure", "Azure Blob"
        GCS = "gcs", "Google Cloud Storage"
        EXTERNAL = "external", "External URL"

    class SourceType(models.TextChoices):
        UPLOAD = "upload", "Upload"
        YOUTUBE = "youtube", "YouTube"
        INSTAGRAM = "instagram", "Instagram"
        VIMEO = "vimeo", "Vimeo"
        FACEBOOK = "facebook", "Facebook"
        URL = "url", "URL"

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="media_assets",)
    folder = models.ForeignKey(MediaFolder, null=True, blank=True, on_delete=models.SET_NULL, related_name="assets",)
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255, blank=True)
    asset_type = models.CharField(max_length=20, choices=AssetType.choices,)
    source_type = models.CharField(max_length=20, choices=SourceType.choices, default=SourceType.UPLOAD,)
    storage_provider = models.CharField(max_length=30, choices=StorageProvider.choices, default=StorageProvider.LOCAL,)
    file = models.FileField(upload_to="assets/", blank=True, null=True,)
    external_url = models.URLField(blank=True)
    provider_asset_id = models.CharField(max_length=255, blank=True,)
    mime_type = models.CharField(max_length=100, blank=True,)
    file_size = models.BigIntegerField(default=0,)
    width = models.PositiveIntegerField(null=True, blank=True,)
    height = models.PositiveIntegerField( null=True, blank=True,)
    duration = models.PositiveIntegerField(null=True, blank=True, help_text="Duration in seconds",)
    alt_text = models.CharField( max_length=255, blank=True,)
    caption = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True,)
    checksum = models.CharField(max_length=128, blank=True,)
    is_public = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["tenant", "asset_type"]),
            models.Index(fields=["storage_provider"]),
            models.Index(fields=["source_type"]),
        ]

    def __str__(self):
        return self.title or self.name

class MediaVariant(BaseModel):

    class VariantType(models.TextChoices):
        ORIGINAL = "original", "Original"
        THUMBNAIL = "thumbnail", "Thumbnail"
        SMALL = "small", "Small"
        MEDIUM = "medium", "Medium"
        LARGE = "large", "Large"
        MOBILE = "mobile", "Mobile"
        DESKTOP = "desktop", "Desktop"
        RETINA_2X = "retina_2x", "Retina 2x"
        RETINA_3X = "retina_3x", "Retina 3x"
        WEBP = "webp", "WebP"
        AVIF = "avif", "AVIF"
        WATERMARK = "watermark", "Watermarked"
        CROPPED = "cropped", "Cropped"
        AI_ENHANCED = "ai_enhanced", "AI Enhanced"
        CUSTOM = "custom", "Custom"

    class ProcessingStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        PROCESSING = "processing", "Processing"
        READY = "ready", "Ready"
        FAILED = "failed", "Failed"

    asset = models.ForeignKey(MediaAsset, related_name="variants", on_delete=models.CASCADE,)
    variant_type = models.CharField(max_length=30, choices=VariantType.choices,)
    file = models.FileField(upload_to="assets/variants/", blank=True, null=True,)
    mime_type = models.CharField(max_length=100, blank=True,)
    width = models.PositiveIntegerField(null=True, blank=True,)
    height = models.PositiveIntegerField(null=True, blank=True,)
    file_size = models.BigIntegerField(default=0)
    processing_status = models.CharField(max_length=20, choices=ProcessingStatus.choices, default=ProcessingStatus.PENDING,)
    transformation = models.JSONField(default=dict, blank=True,)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["asset", "variant_type"],
                name="uq_media_variant_asset_type",
            ),
        ]



class MediaReference(BaseModel):

    class ReferenceType(models.TextChoices):
        PRIMARY = "primary", "Primary"
        GALLERY = "gallery", "Gallery"
        LOGO = "logo", "Logo"
        FAVICON = "favicon", "Favicon"
        HERO = "hero", "Hero"
        BACKGROUND = "background", "Background"
        ICON = "icon", "Icon"
        THUMBNAIL = "thumbnail", "Thumbnail"
        ATTACHMENT = "attachment", "Attachment"
        VIDEO = "video", "Video"
        DOCUMENT = "document", "Document"
        OTHER = "other", "Other"


    asset = models.ForeignKey(MediaAsset, related_name="references", on_delete=models.CASCADE,)
    # Generic relationship
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,)
    object_id = models.UUIDField()
    content_object = GenericForeignKey( "content_type", "object_id",)

    reference_type = models.CharField( max_length=30, choices=ReferenceType.choices,default=ReferenceType.PRIMARY,)
    order = models.PositiveIntegerField(default=0)
    metadata = models.JSONField(default=dict, blank=True,)

    class Meta:
        ordering = [
            "order",
            "-created_at",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "asset",
                    "content_type",
                    "object_id",
                    "reference_type",
                ],
                name="uq_media_reference_target_type",
            )
        ]
        indexes = [
            models.Index(
                fields=[
                    "content_type",
                    "object_id",
                ],
                name="idx_media_reference_object",
            )
        ]

    def __str__(self):
        return f"{self.asset} ({self.reference_type})"
