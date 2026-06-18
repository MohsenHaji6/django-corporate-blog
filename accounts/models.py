from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .manager import CustomUserManager
from .validators import validate_phone_number


class CustomUser(AbstractUser):
    username = None

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    phone_number = models.CharField(
        _("mobile number"),
        max_length=11,
        unique=True,
        validators=[validate_phone_number],
    )

    objects = CustomUserManager()

    def __str__(self):
        return self.get_full_name()
