from django.test import TestCase

from catalog.models import Product, ProductVariant


class BaseCatalogTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.product = Product.objects.create(
            name="test product",
        )

        cls.product_variant1 = ProductVariant.objects.create(
            product=cls.product,
            title="test product variant 1",
            unit_price=100.00,
            image="test.jpg",
        )

        cls.product_variant2 = ProductVariant.objects.create(
            product=cls.product,
            title="test product variant 2",
            unit_price=100.00,
        )
