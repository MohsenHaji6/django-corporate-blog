from django.contrib import admin
from django.db.models import Count, Q
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.utils.html import format_html

from .forms import ProductVariantAdminForm
from .models import Product, ProductVariant


class ProductVariantInline(admin.TabularInline):
    """Tabular Inline View for ProductVariant"""

    model = ProductVariant
    min_num = 0
    max_num = 10
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "product_variant_count", "order")
    search_fields = ("name",)
    inlines = (ProductVariantInline,)
    list_filter = ("is_active",)
    list_editable = ("is_active",)
    list_per_page = 20

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return (
            super()
            .get_queryset(request)
            .annotate(variant_count=Count("variants", filter=Q(variants__is_active=True)))
        )

    @admin.display(description="#Active Variants")
    def product_variant_count(self, obj):
        return obj.variant_count


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    form = ProductVariantAdminForm
    list_display = (
        "product",
        "title",
        "unit_price",
        "in_stock",
        "is_active",
        "show_image",
    )
    list_display_links = ("title",)
    list_per_page = 20
    list_editable = ("unit_price", "in_stock", "is_active")
    list_filter = (
        "in_stock",
        "is_active",
        "product",
    )
    autocomplete_fields = ("product",)
    readonly_fields = ("thumbnail",)
    fieldsets = (
        ("Product", {"fields": ("product", "title", "is_active")}),
        ("Features", {"fields": ("features",)}),
        ("Stock", {"fields": ("unit_price", "in_stock")}),
        ("Media", {"fields": ("image", "thumbnail")}),
        ("Ordering", {"fields": ("order",)}),
        ("Metadata", {"fields": ("updated_at",)}),
    )
    search_fields = ("product", "title")

    @admin.display(description="Image")
    def show_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100px">', obj.image.url)
        return "-"

    @admin.display(description="Thumbnail")
    def thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="250px">', obj.image.url)
        return "-"
