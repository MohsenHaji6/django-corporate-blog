from django.test import TestCase

from catalog.models import Product, ProductVariant
from core.models.site_setting import SiteSetting


class BaseCatalogTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        SiteSetting.objects.create(
            site_title="test site title",
            site_description="test site description",
            meta_title="test meta title",
            meta_description="test meta description",
            hero_title="test hero title",
            hero_text="test hero text",
            hero_image="test-hero-image.jpg",
            logo="test-logo.jpg",
            favicon="test-favicon.jpg",
            email="test@mail.com",
        )
        cls.product = Product.objects.create(name="test")
        cls.product_variant1 = ProductVariant.objects.create(
            product=cls.product,
            title="test variant",
            unit_price=100.00,
            image="test.jpg",
        )
        cls.product_variant2 = ProductVariant.objects.create(
            product=cls.product,
            title="test variant2",
            unit_price=100.00,
        )

    def create_product(self, name="test product", is_active=True):
        Product.objects.create(
            name=name,
            is_active=is_active,
        )

    def create_product_variant(
        self, product=None, title="test product variant", is_active=True
    ):
        ProductVariant.objects.create(
            product=product if product else self.product,
            title=title,
            unit_price=100.00,
            is_active=is_active,
        )
