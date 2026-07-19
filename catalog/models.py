from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    name = models.CharField(_("Name"), max_length=150, unique=True)
    is_active = models.BooleanField(_("Is Active"), default=True)
    order = models.PositiveSmallIntegerField(_("Order"), default=0)

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

        ordering = ["order", "name"]

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
    features = models.TextField(_("Features"), blank=True)
    unit_price = models.DecimalField(_("Unit Price"), decimal_places=2, max_digits=10)
    in_stock = models.BooleanField(_("In Stock"), default=True)
    image = models.ImageField(_("Image"), upload_to="product/", blank=True, null=True)
    updated_at = models.DateField(_("Update At"), default=timezone.now)
    is_active = models.BooleanField(_("Is Active"), default=True)
    order = models.PositiveSmallIntegerField(_("Order"), default=0)

    class Meta:
        verbose_name = _("Product Variant")
        verbose_name_plural = _("Product Variants")

        ordering = ["order", "title"]

    def __str__(self):
        return self.title
