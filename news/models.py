from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from accounts.validators import validate_phone_number


class Subscriber(models.Model):
    name = models.CharField(_("Name"), max_length=50)
    phone_number = models.CharField(
        _("Phone Number"), max_length=11, unique=True, validators=[validate_phone_number]
    )
    datetime_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Subscriber")
        verbose_name_plural = _("Subscribers")

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(_("Name"), max_length=150, unique=True)

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return self.name


class ProductVariant(models.Model):
    product = models.ForeignKey(
        Product,
        verbose_name=_("Product"),
        on_delete=models.CASCADE,
        related_name="variants",
    )
    title = models.CharField(_("Title"), max_length=150)
    attribute = models.TextField(_("attribute"), blank=True)
    unit_price = models.PositiveBigIntegerField(_("Unit Price"))
    in_stock = models.BooleanField(_("In Stock"), default=True)
    image = models.ImageField(_("Image"), upload_to="product/", blank=True, null=True)
    updated_date = models.DateField(_("Update Date"), default=timezone.now)

    class Meta:
        verbose_name = _("Product Variant")
        verbose_name_plural = _("Product Variants")

    def __str__(self):
        return self.title
