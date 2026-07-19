from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.enums import TextChoices
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from treebeard.mp_tree import MP_Node

User = get_user_model()


class Category(MP_Node):
    name = models.CharField(_("Name"), max_length=50)
    slug = models.SlugField(_("Slug"), unique=True, blank=True, allow_unicode=True)
    description = models.TextField(_("Description"), blank=True)
    meta_title = models.CharField(_("Meta Title"), max_length=70, blank=True)
    meta_description = models.CharField(_("Meta Description"), max_length=160, blank=True)
    image = models.ImageField(_("Cover Image"), upload_to="blog/cat/", blank=True)

    node_order_by = ["name"]

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        source = self.slug if self.slug else self.name
        self.slug = slugify(source, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog:category", kwargs={"slug": self.slug})


class Tag(models.Model):
    name = models.CharField(_("Name"), max_length=50)
    slug = models.SlugField(_("Slug"), unique=True, blank=True, allow_unicode=True)
    description = models.TextField(_("Description"), blank=True)
    meta_title = models.CharField(_("Meta Title"), max_length=70, blank=True)
    meta_description = models.CharField(_("Meta Description"), max_length=160, blank=True)

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        source = self.slug if self.slug else self.name
        self.slug = slugify(source, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog:tag", kwargs={"slug": self.slug})


class Article(models.Model):
    class Status(TextChoices):
        DRAFT = "DR", _("Draft")
        PUBLISHED = "PU", _("Published")
        SCHEDULED = "SC", _("Scheduled")
        ARCHIVED = "AR", _("Archived")

    title = models.CharField(_("Title"), max_length=150)
    slug = models.SlugField(_("Slug"), unique=True, blank=True, allow_unicode=True)
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name=_("Author"),
        related_name="articles",
    )
    content = models.TextField(_("Content"))
    summary = models.TextField(_("Summary"), blank=True)
    meta_title = models.CharField(_("Meta Title"), max_length=70, blank=True)
    meta_description = models.CharField(_("Meta Description"), max_length=160, blank=True)
    image = models.ImageField(_("Cover Image"), upload_to="blog/")
    image_alt_text = models.CharField(_("Image Alt Text"), max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    published_at = models.DateTimeField(_("Published At"), default=timezone.now)
    status = models.CharField(
        _("Status"), max_length=2, choices=Status, default=Status.DRAFT
    )
    views_count = models.PositiveIntegerField(default=0)
    category_main = models.ForeignKey(
        Category,
        verbose_name=_("Category main"),
        on_delete=models.PROTECT,
        related_name="articles",
    )
    categories = models.ManyToManyField(Category, verbose_name=_("Categories"), blank=True)
    
    tags = models.ManyToManyField(
        Tag, verbose_name=_("Tags"), blank=True, related_name="articles"
    )

    class Meta:
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")

        ordering = ["-updated_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):

        source = self.slug if self.slug else self.title
        self.slug = slugify(source, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"slug": self.slug})


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
    email = models.EmailField(_("Email"), unique=True)
    body = models.CharField(_("Body"), max_length=400)
    status = models.CharField(
        _("Status"), max_length=2, choices=Status, default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
