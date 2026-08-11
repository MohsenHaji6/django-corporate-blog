from django.urls import reverse

from core.models.page import Page

from .base import BaseCatalogTest


class CatalogViewTest(BaseCatalogTest):
    def test_status_code_200(self):
        response = self.client.get(reverse("catalog:catalog"))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        response = self.client.get(reverse("catalog:catalog"))
        self.assertTemplateUsed(response, "catalog/catalog.html")

    def test_uses_correct_page_for_catalog(self):
        Page.objects.create(
            page_type=Page.PageType.CATALOG,
            title="test catalog",
        )
        response = self.client.get(reverse("catalog:catalog"))
        page = response.context["page"]

        self.assertEqual(page.page_type, Page.PageType.CATALOG)

    def test_shows_only_product_is_active(self):
        self.create_product(is_active=False)
        response = self.client.get(reverse("catalog:catalog"))
        products = []
        for product in response.context["products"]:
            products.append(product["name"])

        self.assertEqual(len(products), 1)

    def test_shows_only_product_variant_is_active(self):
        self.create_product_variant(is_active=False)
        response = self.client.get(reverse("catalog:catalog"))

        variants = []
        for product in response.context["products"]:
            for variant in product["variants"]:
                variants.append(variant)

        self.assertEqual(len(variants), 2)
