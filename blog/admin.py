from django.contrib import admin
from django.utils.safestring import mark_safe
from treebeard.admin import TreeAdmin

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
        "slug",
        "author",
        "meta_title",
        "meta_description",
        "status",
        "category_main",
    ]
    prepopulated_fields = {
        "slug": [
            "title",
        ],
    }
    inlines = [CommentInline]

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)

        article = form.instance

        if article.category_main:
            article.categories.add(article.category_main)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "description"]
    search_fields = ["name"]
    prepopulated_fields = {
        "slug": [
            "name",
        ]
    }
