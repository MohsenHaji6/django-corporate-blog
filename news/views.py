from django.http import JsonResponse
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from .forms import SubscriberForm
from .models import Product


def subscriber_view(request):
    if request.method == "POST":
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse(
                {"success": True, "message": _("Subscription successful.")}, status=200
            )
        return JsonResponse({"success": False, "errors": form.errors}, status=400)

    return JsonResponse(
        {"success": False, "message": _("Invalid request method.")}, status=405
    )


def pricing_view(request):
    breadcrumbs = [
        {"title": _("Home"), "url": "/"},
        {"title": _("Pricing")},
    ]
    products = Product.objects.prefetch_related("variants").all()
    product_data = []

    for product in products:
        variants = product.variants.all()  # type: ignore
        variant_data = [
            {
                "title": variant.title,
                "attribute": variant.attribute,
                "unit_price": variant.unit_price,
                "in_stock": variant.in_stock,
                "image": variant.image.url if variant.image else None,
                "updated_date": variant.updated_date,
            }
            for variant in variants
        ]
        product_data.append({"name": product.name, "variants": variant_data})

    return render(
        request,
        "news/pricing.html",
        {"products": product_data, "breadcrumbs": breadcrumbs},
    )
