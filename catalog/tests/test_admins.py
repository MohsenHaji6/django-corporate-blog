from django.contrib import admin
from django.test import RequestFactory

from catalog.admin import ProductAdmin, ProductVariantAdmin
from catalog.models import Product, ProductVariant
from catalog.tests.base import BaseCatalogTest


class ProductAdminTest(BaseCatalogTest):
    def test_variant_count(self):

        request = RequestFactory().get("/admin/")
        admin_instance = ProductAdmin(Product, admin.site)
        queryset = admin_instance.get_queryset(request)
        product = queryset.get(pk=self.product.pk)

        self.assertEqual(product.variant_count, 2)


class ProductVariantAdminTest(BaseCatalogTest):
    def test_show_image_with_image(self):
        admin_instance = ProductVariantAdmin(ProductVariant, admin.site)
        img = admin_instance.show_image(self.product_variant1)

        self.assertEqual('<img src="/media/test.jpg" width="100px">', img)

    def test_show_image_without_image(self):
        admin_instance = ProductVariantAdmin(ProductVariant, admin.site)
        img = admin_instance.show_image(self.product_variant2)

        self.assertEqual("-", img)

    def test_thumbnail_with_image(self):
        admin_instance = ProductVariantAdmin(ProductVariant, admin.site)
        img = admin_instance.thumbnail(self.product_variant1)

        self.assertEqual('<img src="/media/test.jpg" width="250px">', img)

    def test_thumbnail_without_image(self):
        admin_instance = ProductVariantAdmin(ProductVariant, admin.site)
        img = admin_instance.thumbnail(self.product_variant2)

        self.assertEqual("-", img)
