from django.db import models
from django.utils.translation import gettext_lazy as _


class Page(models.Model):
    slug = models.SlugField(_("Slug"), unique=True, allow_unicode=True)
    description = models.TextField(_("Description"))
    short_description = models.TextField(
        _("Short Description"),
        help_text="To display on the home page of the site",
        blank=True,
    )

    class Meta:
        verbose_name = _("Page")
        verbose_name_plural = _("Pages")

    def __str__(self) -> str:
        return self.slug

