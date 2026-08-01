from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.validators import validate_phone_number


class ContactMessage(models.Model):
    name = models.CharField(_("Name"), max_length=50)
    phone_number = models.CharField(
        _("Phone Number"), max_length=11, validators=[validate_phone_number]
    )
    message = models.CharField(_("Message"), max_length=255)

    email_sent = models.BooleanField(_("Email Sent"), default=False)
    sms_sent = models.BooleanField(_("SMS Sent"), default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Contact Message")
        verbose_name_plural = _("Contact Messages")
