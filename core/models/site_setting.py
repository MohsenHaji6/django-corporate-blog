from django.db import models
from django.db.models.constraints import UniqueConstraint
from django.utils.translation import gettext_lazy as _


class SiteSetting(models.Model):
    title = models.CharField(_("Site Title"), max_length=70)
    description = models.CharField(_("Site Description"), max_length=160)
    logo = models.ImageField(_("Logo"), upload_to="logo/", max_length=50)
    favicon = models.ImageField(_("Favicon"), upload_to="logo/", max_length=50)
    email = models.EmailField(_("Site Email"), max_length=254)
    answer_hours = models.CharField(_("Answering Hours"), max_length=50, blank=True)
    copyright = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = _("Site Setting")
        verbose_name_plural = _("Site Settings")

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)


class PhoneNumber(models.Model):
    use_for = models.CharField(_("Use For"), max_length=50)
    phone_number = models.CharField(_("Phone Number"), max_length=20)
    icon = models.ImageField(_("Icon"), upload_to="icons/", max_length=50, blank=True)
    display_order = models.PositiveSmallIntegerField(default=0)
    is_primary = models.BooleanField(_("Is Primary"), default=False)
    is_active = models.BooleanField(_("Is Active"), default=True)

    class Meta:
        verbose_name = _("Phone Number")
        verbose_name_plural = _("Phone Numbers")

        constraints = [
            UniqueConstraint(
                fields=["is_primary"],
                condition=models.Q(is_primary=True),
                name="only_one_primary_phone",
            )
        ]

    def __str__(self) -> str:
        return f"{self.use_for}: {self.phone_number}"


class SocialLink(models.Model):
    name = models.CharField(_("Name"), max_length=50)
    url = models.URLField(_("Url"), max_length=254)
    icon = models.ImageField(_("Icon"), upload_to="icons/", max_length=50)
    display_order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(_("Is Active"), default=True)

    class Meta:
        verbose_name = _("Social Link")
        verbose_name_plural = _("Social Links")

    def __str__(self) -> str:
        return self.name


class Address(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    province = models.CharField(_("Province"), max_length=50)
    city = models.CharField(_("City"), max_length=50)
    address = models.CharField(_("Address"), max_length=255)
    is_primary = models.BooleanField(_("Is Primary"), default=False)
    is_active = models.BooleanField(_("Is Active"), default=True)

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")

        constraints = [
            UniqueConstraint(
                fields=["is_primary"],
                condition=models.Q(is_primary=True),
                name="only_one_primary_address",
            )
        ]

    def __str__(self):
        return self.name
