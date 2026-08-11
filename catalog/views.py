from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from core.models import Page

from .models import Product


def catalog_view(request):
    page = Page.objects.filter(page_type=Page.PageType.CATALOG).first()

    breadcrumbs = [
        {"title": _("Home"), "url": "core:home"},
        {"title": _("Catalog")},
    ]
    products = Product.objects.filter(is_active=True).prefetch_related("variants").all()
    product_data = []

    for product in products:
        variants = product.variants.filter(is_active=True).all()  # type: ignore
        variant_data = [
            {
                "title": variant.title,
                "features": variant.features,
                "unit_price": variant.unit_price,
                "in_stock": variant.in_stock,
                "image": variant.image.url if variant.image else None,
                "updated_at": variant.updated_at,
            }
            for variant in variants
        ]
        product_data.append({"name": product.name, "variants": variant_data})

    return render(
        request,
        "catalog/catalog.html",
        {"products": product_data, "breadcrumbs": breadcrumbs, "page": page},
    )
