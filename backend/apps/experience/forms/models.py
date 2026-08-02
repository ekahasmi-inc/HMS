from django.db import models

from apps.platform.common.models import BaseModel

class Form(BaseModel):
    """
    Dynamic form definition.
    """

    class FormType(models.TextChoices):
        CONTACT = "contact", "Contact"
        BOOKING = "booking", "Booking Enquiry"
        RESTAURANT = "restaurant", "Restaurant Reservation"
        EVENT = "event", "Event"
        NEWSLETTER = "newsletter", "Newsletter"
        CAREER = "career", "Career"
        FEEDBACK = "feedback", "Feedback"
        CUSTOM = "custom", "Custom"

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"
        ARCHIVED = "archived", "Archived"

    tenant = models.ForeignKey("tenants.Tenant", on_delete=models.CASCADE, related_name="forms",)
    website = models.ForeignKey( "website.Website", on_delete=models.CASCADE, related_name="forms",)
    name = models.CharField( max_length=200,)
    slug = models.SlugField( max_length=200,)
    form_type = models.CharField(max_length=30, choices=FormType.choices, default=FormType.CONTACT,)
    title = models.CharField( max_length=255,)
    description = models.TextField(blank=True,)
    success_message = models.TextField(blank=True,)
    submit_button_text = models.CharField(max_length=100, default="Submit",)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT,)
    is_active = models.BooleanField(default=True,)
    allow_multiple_submissions = models.BooleanField(default=True,)
    require_login = models.BooleanField(default=False,)
    notify_admin = models.BooleanField(default=True,)
    metadata = models.JSONField(default=dict,blank=True,)

    class Meta:
        ordering = ["name"]

        constraints = [
            models.UniqueConstraint(
                fields=["website", "slug"],
                name="uq_form_website_slug",
            ),
        ]

        indexes = [
            models.Index(
                fields=["tenant", "status"],
                name="idx_form_tenant_status",
            ),
            models.Index(
                fields=["website", "slug"],
                name="idx_form_slug",
            ),
        ]

    def __str__(self):
        return self.name