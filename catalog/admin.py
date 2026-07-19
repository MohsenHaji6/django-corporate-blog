from django.contrib import admin

from .models import Product, ProductVariant


class ProductVariantInline(admin.TabularInline):
    """Tabular Inline View for ProductVariant"""

    model = ProductVariant
    min_num = 0
    max_num = 10
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductVariantInline]
