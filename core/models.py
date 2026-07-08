from django.db import models
from django.db.models.enums import TextChoices
from django.utils.translation import gettext_lazy as _


class SiteSetting(models.Model):
    title = models.CharField(_("Site Title"), max_length=70)
    description = models.CharField(_("Site Description"), max_length=160)
    logo = models.ImageField(_("Logo"), upload_to="logo/")
    favicon = models.ImageField(_("Favicon"), upload_to="logo/")
    email = models.EmailField(_("Site Email"), max_length=254)
    about_text = models.TextField(_("About Text"))
    privacy_policy = models.TextField(_("Privacy Policy"))

    class Meta:
        verbose_name = _("Site Setting")
        verbose_name_plural = _("Site Settings")

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)


class PhoneNumber(models.Model):
    class Type(TextChoices):
        LANDLINE = "LI", _("Landline")
        MOBILE_PHONE = "MP", _("Mobile Phone")

    class UseFor(TextChoices):
        MANAGEMENT = "MGT", _("Management")
        SITE_SUPPORT = "SIS", _("Site Support")
        SALES_SUPPORT = "SAS", _("Sales Support")

    site_settings = models.ForeignKey(
        SiteSetting,
        on_delete=models.CASCADE,
        related_name="phone_numbers",
    )
    type = models.CharField(
        _("Phone Type"), max_length=2, choices=Type, default=Type.LANDLINE
    )

    use_for = models.CharField(
        _("Use For"), max_length=3, choices=UseFor, default=UseFor.SALES_SUPPORT
    )

    phone_number = models.CharField(_("Phone Number"), max_length=13)

    class Meta:
        verbose_name = _("Phone Number")
        verbose_name_plural = _("Phone Numbers")


class Address(models.Model):
    site_settings = models.ForeignKey(
        SiteSetting,
        on_delete=models.CASCADE,
        related_name="addresses",
    )
    name = models.CharField(_("Name"), max_length=100)
    province = models.CharField(_("Province"), max_length=50)
    city = models.CharField(_("City"), max_length=50)
    address = models.CharField(_("Address"), max_length=255)

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")


class SocialMedia(models.Model):
    class Name(TextChoices):
        INSTAGRAM = "INS", _("Instagram")
        TELEGRAM = "TEL", _("Telegram")
        WHATSAPP = "WHT", _("WhatsApp")

    site_settings = models.ForeignKey(
        SiteSetting, on_delete=models.CASCADE, related_name="social_medias"
    )
    name = models.CharField(_("Name"), max_length=3, choices=Name, default=Name.INSTAGRAM)
    url = models.URLField(_("Url"), max_length=254)

    class Meta:
        verbose_name = _("Social Media")
        verbose_name_plural = _("Social Medias")
