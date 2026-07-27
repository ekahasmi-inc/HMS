from django.contrib.auth.models import AbstractUser

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