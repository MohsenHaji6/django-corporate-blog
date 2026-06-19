from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from treebeard.mp_tree import MP_Node

User = get_user_model()


class Category(MP_Node):
    name = models.CharField(_("Name"), max_length=50)
    slug = models.SlugField(_("Slug"), unique=True)
    description = models.TextField(_("Description"), blank=True)
    meta_title = models.CharField(_("Meta Title"), max_length=70, blank=True)
    meta_description = models.CharField(_("Meta Description"), max_length=160, blank=True)
    image = models.ImageField(_("Image Cover"), upload_to="blog/cat/", blank=True)

    node_order_by = ["name"]

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(_("Name"), max_length=50)
    slug = models.SlugField(_("Slug"), unique=True)
    description = models.TextField(_("Description"), blank=True)
    meta_title = models.CharField(_("Meta Title"), max_length=70, blank=True)
    meta_description = models.CharField(_("Meta Description"), max_length=160, blank=True)

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(_("Title"), max_length=150)
    slug = models.SlugField(_("Slug"), unique=True)
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("Author"),
        related_name="articles",
    )
    body = models.TextField(_("Body"))
    meta_title = models.CharField(_("Meta Title"), max_length=70, blank=True)
    meta_description = models.CharField(_("Meta Description"), max_length=160, blank=True)
    image = models.ImageField(_("Image Cover"), upload_to="blog/")
    datetime_created = models.DateTimeField(_("Datetime Created"), auto_now_add=True)
    datetime_update = models.DateTimeField(_("Datetime Last Update"), auto_now=True)
    update_note = models.CharField(
        _("Update Note"), max_length=255, help_text="Status of the text to date"
    )
    datetime_publish = models.DateTimeField(_("Datetime Publish"), default=timezone.now)
    status_publish = models.BooleanField(_("Status Publish"), default=False)
    category_main = models.ForeignKey(
        Category,
        verbose_name=_("Category main"),
        on_delete=models.PROTECT,
        related_name="articles",
    )
    categories = models.ManyToManyField(Category, verbose_name=_("Categories"), blank=True)
    tag = models.ManyToManyField(
        Tag, verbose_name=_("Tag"), blank=True, related_name="articles"
    )

    class Meta:
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")

    def __str__(self):
        return self.title

    def clean(self):
        if self.categories.filter(pk=self.category_main.pk).exists():
            raise ValidationError(
                "The main category should not be selected in subcategories."
            )


class Comment(models.Model):
    class Status(models.TextChoices):
        PENDING = "PE", _("Pending")
        APPROVED = "AP", _("Approved")
        SPAM = "SP", _("Spam")

    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name=_("Article"),
    )
    name = models.CharField(_("Name"), max_length=50)
    email = models.CharField(_("Email"), unique=True)
    body = models.CharField(_("Body"), max_length=400)
    status = models.CharField(
        _("Status"), max_length=2, choices=Status, default=Status.PENDING
    )
    datetime_created = models.DateTimeField(auto_now_add=True)
