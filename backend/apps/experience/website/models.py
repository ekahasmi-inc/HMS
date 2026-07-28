from django.db import models

from apps.platform.common.models import BaseModel
from apps.platform.tenants.models import Tenant


class Website(BaseModel):
    """
    Root website for a tenant.
    """
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        PUBLISHED = "PUBLISHED", "Published"
        MAINTENANCE = "MAINTENANCE", "Maintenance"

    tenant = models.OneToOneField(Tenant, on_delete=models.CASCADE, related_name="website",)
    name = models.CharField(max_length=200,)
    title = models.CharField(max_length=255, blank=True,)
    tagline = models.CharField(max_length=255, blank=True,)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT, db_index=True,)
    homepage = models.CharField(max_length=255, default="/", help_text="Homepage route",)
    is_active = models.BooleanField(default=True, db_index=True,)

    class Meta:
        db_table = "websites"
        ordering = ["name"]

    def __str__(self):
        return self.name

class WebsiteTheme(BaseModel):
    """
    Visual theme configuration for a website.
    """

    class ThemeMode(models.TextChoices):
        LIGHT = "LIGHT", "Light"
        DARK = "DARK", "Dark"
        AUTO = "AUTO", "Auto"

    website = models.OneToOneField(Website, on_delete=models.CASCADE, related_name="theme",)
    theme_name = models.CharField(max_length=100, default="Default",)
    theme_slug = models.SlugField(max_length=100, db_index=True,)
    mode = models.CharField( max_length=10, choices=ThemeMode.choices, default=ThemeMode.LIGHT,)
    version = models.CharField(max_length=20, default="1.0",)
    is_active = models.BooleanField(default=True, db_index=True,)

    class Meta:
        db_table = "website_themes"
        ordering = ["theme_name"]

    def __str__(self):
        return f"{self.website.name} - {self.theme_name}"


class WebsiteMenu(BaseModel):
    """
    Navigation menu belonging to a website.
    """

    class MenuLocation(models.TextChoices):
        HEADER = "HEADER", "Header"
        FOOTER = "FOOTER", "Footer"
        MOBILE = "MOBILE", "Mobile"
        SIDEBAR = "SIDEBAR", "Sidebar"
        CUSTOM = "CUSTOM", "Custom"

    website = models.ForeignKey(Website, on_delete=models.CASCADE, related_name="menus",)
    name = models.CharField(max_length=100,)
    slug = models.SlugField(max_length=100,)
    location = models.CharField(max_length=20, choices=MenuLocation.choices, default=MenuLocation.HEADER, db_index=True,)
    is_active = models.BooleanField(default=True, db_index=True,)

    class Meta:
        db_table = "website_menus"

        ordering = [
            "name",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=["website", "slug"],
                name="uq_website_menu_slug",
            )
        ]

    def __str__(self):
        return f"{self.website.name} - {self.name}"

class WebsiteMenuItem(BaseModel):
    """
    Individual navigation item belonging to a menu.
    """
    class LinkType(models.TextChoices):
        INTERNAL = "INTERNAL", "Internal"
        EXTERNAL = "EXTERNAL", "External"

    menu = models.ForeignKey(WebsiteMenu, on_delete=models.CASCADE, related_name="items",)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name="children",)
    title = models.CharField(max_length=100,)
    slug = models.SlugField(max_length=100,)
    url = models.CharField(max_length=500, help_text="Internal path or external URL.",)
    link_type = models.CharField(max_length=20, choices=LinkType.choices, default=LinkType.INTERNAL,)
    icon = models.CharField(max_length=100, blank=True,)
    display_order = models.PositiveIntegerField(default=0, db_index=True,)
    open_in_new_tab = models.BooleanField(default=False,)
    is_visible = models.BooleanField(default=True, db_index=True,)

    class Meta:
        db_table = "website_menu_items"

        ordering = [
            "display_order",
            "title",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=["menu", "slug"],
                name="uq_menu_item_slug",
            )
        ]

    def __str__(self):
        return self.title