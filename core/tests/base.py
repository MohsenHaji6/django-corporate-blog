from django.test import TestCase

from core.models import Page, PhoneNumber, SiteSetting
from core.models.site_setting import Address


class BaseCoreTest(TestCase):
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

    def create_page(self, page_type):
        Page.objects.create(page_type=page_type, title="test page")

    def create_phone_number(self, use_for="for test", is_primary=False, is_active=True):
        PhoneNumber.objects.create(
            use_for=use_for,
            phone_number="+989121111111",
            is_primary=is_primary,
            is_active=is_active,
        )

    def create_address(self, name="test name", is_primary=False, is_active=True):
        Address.objects.create(
            name=name,
            province="test province",
            city="test city",
            address="test address",
            is_primary=is_primary,
            is_active=is_active,
        )
