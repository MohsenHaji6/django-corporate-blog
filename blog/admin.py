from django.contrib import admin, messages
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from treebeard.admin import TreeAdmin

from .admin_filters import CategoryDropdownFilter
from .forms import ArticleAdminForm, CategoryAdminForm
from .models import Article, Category, Comment, Tag


@admin.register(Category)
class CategoryAdmin(TreeAdmin):
    list_display = ["name", "slug", "cover_image"]
    list_display_links = ["slug"]
    search_fields = ["name"]
    prepopulated_fields = {
        "slug": [
            "name",
        ]
    }
    form = CategoryAdminForm
    exclude = ["path", "depth", "numchild"]

    @admin.display(description="Image")
    def cover_image(self, obj):
        if obj.image:
            return mark_safe(
                f'<img src="{obj.image.url}" style="max-width:70px; max-height:70px">'
            )
        return "-"


class CommentInline(admin.TabularInline):
    """Tabular Inline View for Comment"""

    model = Comment
    min_num = 0
    max_num = 10
    extra = 1


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    class Media:
        js = ("admin/js/meta_title.js",)

    form = ArticleAdminForm
    list_display = [
        "title",
        "category_main",
        "status",
        "author",
        "published_at",
        "updated_at",
    ]
    list_per_page = 15
    prepopulated_fields = {
        "slug": [
            "title",
        ],
    }
    list_filter = [
        "status",
        "published_at",
        CategoryDropdownFilter,
    ]
    search_fields = ["title", "summary"]
    list_editable = ["status"]

    inlines = [CommentInline]
    actions = ["publish_selected", "unpublish_selected"]
    readonly_fields = [
        "author",
        "created_at",
        "updated_at",
        "views_count",
        "thumbnail",
    ]
    autocomplete_fields = ["category_main"]
    filter_horizontal = [
        "tags",
        "categories",
    ]

    fieldsets = (
        (
            "Article",
            {
                "fields": (
                    "title",
                    "slug",
                    "author",
                    "status",
                )
            },
        ),
        (
            "Content",
            {
                "fields": (
                    "content",
                    "summary",
                )
            },
        ),
        (
            "Categories & Tags",
            {
                "fields": (
                    "category_main",
                    "categories",
                    "tags",
                )
            },
        ),
        (
            "Media",
            {
                "fields": (
                    "image",
                    "image_alt_text",
                    "thumbnail",
                )
            },
        ),
        (
            "SEO",
            {
                "classes": ("collapse",),
                "fields": (
                    "meta_title",
                    "meta_description",
                ),
            },
        ),
        (
            "Dates & Statistics",
            {
                "classes": ("collapse",),
                "fields": (
                    "published_at",
                    "created_at",
                    "updated_at",
                    "views_count",
                ),
            },
        ),
    )

    @admin.action(description="Publish selected Articles")
    def publish_selected(self, request, queryset):
        update_count = queryset.update(status="PU")
        self.message_user(
            request,
            f"{update_count} of articles published.",
            messages.SUCCESS,  # For choose a color
        )

    @admin.action(description="Unpublish selected Articles")
    def unpublish_selected(self, request, queryset):
        update_count = queryset.update(status="AR")
        self.message_user(
            request,
            f"{update_count} of articles unpublished.",
            messages.ERROR,  # For choose a color
        )

    def save_related(self, request, form, formsets, change):

        article = form.instance

        if article.category_main:
            article.categories.add(article.category_main)

        super().save_related(request, form, formsets, change)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user

        super().save_model(request, obj, form, change)

    @admin.display(description="Thumbnail")
    def thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="250px" height="250px" style="object-fit:cover;'
                'border-radius:6px;" />',
                obj.image.url,
            )
        return "-"


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "description"]
    search_fields = ["name"]
    prepopulated_fields = {
        "slug": [
            "name",
        ]
    }


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["name", "body", "status"]
