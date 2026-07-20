from django.db import models
from django.utils.translation import gettext_lazy as _


class Page(models.Model):
    class PageType(models.TextChoices):
        CONTACT = "CO", _("Contact")
        ABOUT = "AB", _("About")
        PRIVACY = "PR", _("Privacy Policy")
        CATALOG = "CA", _("Catalog")

    page_type = models.CharField(
        _("Page Type"), max_length=2, choices=PageType.choices, unique=True
    )
    title = models.CharField(_("title"), max_length=255)
    description = models.TextField(_("Description"), blank=True)
    short_description = models.TextField(
        _("Short Description"),
        help_text=_("Optional short text for places like the Home page."),
        blank=True,
    )
    meta_title = models.CharField(_("Meta Title"), max_length=70, blank=True)
    meta_description = models.CharField(_("Meta Description"), max_length=160, blank=True)

    class Meta:
        verbose_name = _("Page")
        verbose_name_plural = _("Pages")

    def __str__(self) -> str:
        return self.get_page_type_display()  # type: ignore
