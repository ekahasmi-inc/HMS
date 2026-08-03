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


class FormField(BaseModel):
    """
    Dynamic field definition for a form.
    """
    class FieldType(models.TextChoices):
        TEXT = "text", "Text"
        TEXTAREA = "textarea", "Textarea"
        EMAIL = "email", "Email"
        PHONE = "phone", "Phone"
        NUMBER = "number", "Number"
        DECIMAL = "decimal", "Decimal"
        DATE = "date", "Date"
        TIME = "time", "Time"
        DATETIME = "datetime", "Date & Time"
        PASSWORD = "password", "Password"
        URL = "url", "URL"
        FILE = "file", "File Upload"
        IMAGE = "image", "Image Upload"
        SELECT = "select", "Select"
        MULTISELECT = "multiselect", "Multi Select"
        RADIO = "radio", "Radio"
        CHECKBOX = "checkbox", "Checkbox"
        BOOLEAN = "boolean", "Boolean"
        HIDDEN = "hidden", "Hidden"

    form = models.ForeignKey("Form", on_delete=models.CASCADE, related_name="fields",)
    name = models.CharField(max_length=100, help_text="Internal field name",)
    label = models.CharField( max_length=255,)
    slug = models.SlugField(max_length=120,)
    field_type = models.CharField(max_length=30, choices=FieldType.choices, default=FieldType.TEXT,)
    placeholder = models.CharField(max_length=255, blank=True,)
    help_text = models.TextField(blank=True,)
    default_value = models.TextField(blank=True,)
    is_required = models.BooleanField(default=False,)
    is_active = models.BooleanField(default=True,)
    is_readonly = models.BooleanField(default=False,)
    is_hidden = models.BooleanField(default=False,)
    display_order = models.PositiveIntegerField(default=0,)
    validation_rules = models.JSONField(default=dict, blank=True, help_text="Validation rules such as min/max, regex, length, etc.",)
    ui_schema = models.JSONField(default=dict, blank=True, help_text="Frontend rendering hints.",)
    choices = models.JSONField(default=list, blank=True, help_text="Options for Select, Radio, Checkbox etc.",)
    conditional_logic = models.JSONField(default=dict, blank=True, help_text="Visibility conditions.",)
    metadata = models.JSONField(default=dict, blank=True,)

    class Meta:
        ordering = ["display_order", "id",]

        constraints = [
            models.UniqueConstraint(
                fields=["form", "slug"],
                name="uq_formfield_form_slug",
            ),
            models.UniqueConstraint(
                fields=["form", "name"],
                name="uq_formfield_form_name",
            ),
        ]

        indexes = [
            models.Index(
                fields=["form", "display_order"],
                name="idx_formfield_order",
            ),
            models.Index(
                fields=["form", "field_type"],
                name="idx_formfield_type",
            ),
        ]

    def __str__(self):
        return f"{self.form.name} - {self.label}"


