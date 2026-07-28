from django.contrib.auth.models import AbstractUser
from django.db import models
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