from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from apps.platform.common.models import BaseModel
from .managers import CustomUserManager

class User(BaseModel, AbstractUser):
    """
    Main Platform user.
    """
    objects = CustomUserManager()
    
    class Meta:
        db_table = "identity_users"
        verbose_name = "User"
        verbose_name_plural = "Users"

class Role(BaseModel):
    """
    Defines user roles in the platform.
    """
    name = models.CharField(max_length=100, unique=True,)
    code = models.SlugField(max_length=100, unique=True, db_index=True,)
    description = models.TextField(blank=True,)
    is_system_role = models.BooleanField(default=False, help_text="Predefined roles that cannot be deleted.",)
    is_active = models.BooleanField(default=True, db_index=True,)

    class Meta:
        db_table = "roles"
        ordering = [
            "name",
        ]

    def __str__(self):
        return self.name

class Permission(BaseModel):
    """
    Defines a single platform permission.
    """
    class Scope(models.TextChoices):
        PLATFORM = "PLATFORM", "Platform"
        TENANT = "TENANT", "Tenant"

    name = models.CharField(max_length=150, unique=True,)
    code = models.SlugField(max_length=150, unique=True, db_index=True, help_text="Example: booking.create",)
    module = models.CharField(max_length=100, db_index=True, help_text="Module name (booking, website, pms, crm, etc.)",)
    scope = models.CharField(max_length=20, choices=Scope.choices, default=Scope.TENANT, db_index=True,)
    description = models.TextField(blank=True,)
    is_system_permission = models.BooleanField(default=True, help_text="Core platform permission.",)
    is_active = models.BooleanField(default=True, db_index=True,)

    class Meta:
        db_table = "permissions"
        ordering = ["module", "code",]

    def __str__(self):
        return self.code

class RolePermission(BaseModel):
    """
    Maps roles to permissions.
    """
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="role_permissions",)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name="role_permissions",)
    is_granted = models.BooleanField( default=True, help_text="Allows future deny/override support.",)

    class Meta:
        db_table = "role_permissions"
        verbose_name = "Role Permission"
        verbose_name_plural = "Role Permissions"

        constraints = [
            models.UniqueConstraint(
                fields=["role", "permission"],
                name="uq_role_permission",
            )
        ]

        ordering = ["role", "permission",]

    def __str__(self):
        return f"{self.role.name} → {self.permission.code}"


class UserRole(BaseModel):
    """
    Assigns roles to users.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_roles",)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="user_roles",)
    tenant = models.ForeignKey("tenants.Tenant", on_delete=models.CASCADE, related_name="user_roles", help_text="Tenant where this role assignment is valid.",)
    is_primary = models.BooleanField(default=False, help_text="Primary role for this tenant.",)
    is_active = models.BooleanField(default=True, db_index=True,)

    class Meta:
        db_table = "user_roles"

        verbose_name = "User Role"
        verbose_name_plural = "User Roles"

        constraints = [
            models.UniqueConstraint(fields=["user", "role", "tenant"], name="uq_user_role_tenant",)
        ]

        ordering = ["tenant", "user", "role",]

    def __str__(self):
        return f"{self.user} → {self.role.name} ({self.tenant.name})"