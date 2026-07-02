from django.contrib import admin

from .models import Product, ProductVariant, Subscriber


class ProductVariantInline(admin.TabularInline):
    """Tabular Inline View for ProductVariant"""

    model = ProductVariant
    min_num = 0
    max_num = 10
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductVariantInline]


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ("name", "phone_number", "datetime_created")
    search_fields = ("name", "phone_number")
