from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.validators import validate_phone_number


class Subscriber(models.Model):
    name = models.CharField(_("Name"), max_length=50)
    phone_number = models.CharField(
        _("Phone Number"), max_length=11, unique=True, validators=[validate_phone_number]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Subscriber")
        verbose_name_plural = _("Subscribers")

    def __str__(self):
        return self.name
