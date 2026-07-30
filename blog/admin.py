from django.contrib import admin, messages
from django.db.models import Count, Q
from django.http import HttpRequest
from django.utils.html import format_html
from treebeard.admin import TreeAdmin

from .admin_filters import CategoryDropdownFilter
from .forms import ArticleAdminForm, CategoryAdminForm, CommentAdminForm, TagAdminForm
from .models import Article, Category, Comment, Tag


@admin.register(Category)
class CategoryAdmin(TreeAdmin):
    list_display = ["name", "slug", "article_count", "cover_image"]
    list_display_links = ["slug"]
    search_fields = ["name"]
    prepopulated_fields = {
        "slug": [
            "name",
        ]
    }
    form = CategoryAdminForm
    exclude = ["path", "depth", "numchild"]
    readonly_fields = ["thumbnail"]
    fieldsets = (
        (
            "Category",
            {
                "fields": (
                    "name",
                    "slug",
                )
            },
        ),
        (
            "Position",
            {
                "fields": (
                    "treebeard_position",
                    "treebeard_ref_node",
                ),
            },
        ),
        (
            "Content",
            {"fields": ("description",)},
        ),
        (
            "Media",
            {
                "fields": (
                    "image",
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
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(
            article_count=Count(
                "articles", filter=Q(articles__status=Article.Status.PUBLISHED)
            )
        )

    @admin.display(description="#Published Articles", ordering="article_count")
    def article_count(self, obj):
        return obj.article_count

    @admin.display(description="Image")
    def cover_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width:70px; max-height:70px">', obj.image.url
            )
        return "-"

    @admin.display(description="Thumbnail")
    def thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="200px" style="object-fit:cover;'
                'border-radius:6px;" />',
                obj.image.url,
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
        update_count = queryset.update(status=Article.Status.PUBLISHED)
        self.message_user(
            request,
            f"{update_count} of articles published.",
            messages.SUCCESS,  # For choose a color
        )

    @admin.action(description="Unpublish selected Articles")
    def unpublish_selected(self, request, queryset):
        update_count = queryset.update(status=Article.Status.ARCHIVED)
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
    list_display = ["name", "slug", "article_count", "description"]
    search_fields = ["name"]
    list_per_page = 20
    prepopulated_fields = {
        "slug": [
            "name",
        ]
    }
    form = TagAdminForm

    def get_queryset(self, request: HttpRequest):

        return (
            super()
            .get_queryset(request)
            .annotate(
                article_count=Count(
                    "articles", filter=Q(articles__status=Article.Status.PUBLISHED)
                )
            )
        )

    @admin.display(description="#Published Article", ordering="article_count")
    def article_count(self, obj):
        return obj.article_count


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    form = CommentAdminForm
    list_display = [
        "name",
        "email",
        "article",
        "status",
        "created_at",
    ]

    search_fields = (
        "name",
        "article__title",
        "email",
        "body",
    )
    list_filter = (
        "status",
        "created_at",
    )
    list_editable = ("status",)
    list_per_page = 20
    date_hierarchy = "created_at"
    readonly_fields = ("created_at",)
    autocomplete_fields = ("article",)

    fieldsets = (
        ("Comment", {"fields": ("article", "status")}),
        ("User", {"fields": ("name", "email")}),
        ("Message", {"fields": ("body",)}),
        ("Metadata", {"fields": ("created_at",)}),
    )

    actions = ("approve_selected", "pending_selected", "spam_selected")

    @admin.display(description="Approve selected comments")
    def approve_selected(self, request, queryset):
        approve_count = queryset.update(status=Comment.Status.APPROVED)

        self.message_user(request, f"{approve_count} comments Approved.", messages.SUCCESS)

    @admin.display(description="Mark selected as Pending")
    def pending_selected(self, request, queryset):
        pending_count = queryset.update(status=Comment.Status.PENDING)

        self.message_user(
            request,
            f"{pending_count} selected comments marked as Pending!",
            messages.WARNING,
        )

    @admin.display(description="Mark selected as Spam")
    def spam_selected(self, request, queryset):
        spam_count = queryset.update(status=Comment.Status.SPAM)

        self.message_user(
            request,
            f"{spam_count} selected comments marked as Spam!",
            messages.ERROR,
        )
