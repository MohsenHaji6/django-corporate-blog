from unittest.mock import patch

from django.urls import reverse

from blog.models import Article
from blog.tests.base import BaseBlogTest
from catalog.models import Product, ProductVariant
from core.models.page import Page

from .base import BaseCoreTest


class HomeViewTest(BaseBlogTest):
    def test_returns_status_code_200(self):
        response = self.client.get(reverse("core:home"))

        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        response = self.client.get(reverse("core:home"))

        self.assertTemplateUsed(response, "core/home.html")

    def test_shows_three_latest_published_articles(self):
        for i in range(5):
            self.create_article(
                title=f"test article {i}",
                status=Article.Status.PUBLISHED,
            )

        response = self.client.get(reverse("core:home"))

        self.assertEqual(len(response.context["articles"]), 3)

    def test_shows_only_in_stock_products(self):
        product = Product.objects.create(name="Product test")
        for i in range(6):
            ProductVariant.objects.create(
                product=product, title=f"test {i}", unit_price=100.00
            )

        response = self.client.get(reverse("core:home"))

        products = response.context["products"]

        for product in products:
            self.assertTrue(product.in_stock)

    def test_get_returns_empty_contact_form(self):
        response = self.client.get(reverse("core:home"))

        form = response.context["contact_form"]

        self.assertFalse(form.is_bound)

    def test_valid_contact_form_redirects(self):
        response = self.client.post(
            reverse("core:home"),
            data={
                "name": "name",
                "phone_number": "09121111111",
                "message": "message in test",
            },
        )

        self.assertRedirects(response, reverse("core:home"))

    def test_invalid_contact_form_returns_errors(self):
        response = self.client.post(
            reverse("core:home"),
            data={},
        )

        form = response.context["contact_form"]

        self.assertTrue(form.errors)
        self.assertEqual(response.status_code, 200)


class AboutViewTest(BaseCoreTest):
    def test_returns_status_code_200(self):
        response = self.client.get(reverse("core:about"))

        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        response = self.client.get(reverse("core:about"))

        self.assertTemplateUsed(response, "core/about.html")

    def test_shows_about_page(self):
        self.create_page(Page.PageType.ABOUT)

        response = self.client.get(reverse("core:about"))

        self.assertEqual(
            response.context["page"].page_type,
            Page.PageType.ABOUT,
        )

    def test_contains_correct_breadcrumbs(self):
        response = self.client.get(reverse("core:about"))

        self.assertListEqual(
            response.context["breadcrumbs"],
            [
                {
                    "title": "Home",
                    "url": reverse("core:home"),
                },
                {
                    "title": "About",
                },
            ],
        )


class ContactViewTest(BaseCoreTest):
    def test_returns_status_code_200(self):
        response = self.client.get(reverse("core:contact"))

        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        response = self.client.get(reverse("core:contact"))

        self.assertTemplateUsed(response, "core/contact.html")

    def test_shows_contact_page(self):
        self.create_page(Page.PageType.CONTACT)

        response = self.client.get(reverse("core:home"))

        self.assertEqual(
            response.context["page"].page_type,
            Page.PageType.CONTACT,
        )

    def test_page_is_none_when_contact_page_does_not_exist(self):
        response = self.client.get(reverse("core:home"))

        self.assertIsNone(response.context["page"])

    def test_shows_only_active_phone_numbers(self):
        self.create_phone_number(is_active=True)
        self.create_phone_number(
            use_for="inactive",
            is_active=False,
        )

        response = self.client.get(reverse("core:contact"))

        phones = response.context["phones"]

        self.assertEqual(len(phones), 1)
        self.assertTrue(phones[0].is_active)

    def test_shows_only_active_addresses(self):
        self.create_address(is_active=True)
        self.create_address(
            name="inactive",
            is_active=False,
        )

        response = self.client.get(reverse("core:contact"))

        addresses = response.context["addresses"]

        self.assertEqual(len(addresses), 1)
        self.assertTrue(addresses[0].is_active)

    def test_get_returns_empty_contact_form(self):
        response = self.client.get(reverse("core:contact"))

        form = response.context["form"]

        self.assertFalse(form.is_bound)

    def test_valid_contact_form_redirects(self):
        response = self.client.post(
            reverse("core:contact"),
            data={
                "name": "name",
                "phone_number": "09121111111",
                "message": "message in test",
            },
        )

        self.assertRedirects(response, reverse("core:contact"))

    def test_invalid_contact_form_returns_errors(self):
        response = self.client.post(
            reverse("core:contact"),
            data={},
        )

        form = response.context["form"]

        self.assertTrue(form.errors)
        self.assertEqual(response.status_code, 200)

    def test_contains_correct_breadcrumbs(self):
        response = self.client.get(reverse("core:contact"))

        self.assertListEqual(
            response.context["breadcrumbs"],
            [
                {
                    "title": "Home",
                    "url": reverse("core:home"),
                },
                {
                    "title": "Contact",
                },
            ],
        )


class SearchViewTest(BaseBlogTest):
    def test_returns_status_code_200(self):
        response = self.client.get(
            reverse("core:search"),
            {"q": "test"},
        )

        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        response = self.client.get(
            reverse("core:search"),
            {"q": "test"},
        )

        self.assertTemplateUsed(response, "core/search.html")

    @patch("core.views.search")
    def test_passes_query_to_search_service(self, mock_search):
        mock_search.return_value = []

        self.client.get(
            reverse("core:search"),
            {"q": "django"},
        )

        mock_search.assert_called_once()

        args, kwargs = mock_search.call_args

        self.assertEqual(args[0], "django")
        self.assertEqual(args[1].GET["q"], "django")

    @patch("core.views.search")
    def test_passes_search_results_to_template(self, mock_search):
        article = self.create_article(
            title="test article",
            status=Article.Status.PUBLISHED,
        )

        expected_results = [article]
        mock_search.return_value = expected_results

        response = self.client.get(
            reverse("core:search"),
            {"q": "django"},
        )

        self.assertEqual(
            response.context["articles"],
            expected_results,
        )

    def test_returns_query_in_context(self):
        response = self.client.get(
            reverse("core:search"),
            {"q": "django"},
        )

        self.assertEqual(response.context["query"], "django")


class PrivacyViewTest(BaseCoreTest):
    def test_returns_status_code_200(self):
        response = self.client.get(reverse("core:privacy"))

        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        response = self.client.get(reverse("core:privacy"))

        self.assertTemplateUsed(response, "core/privacy.html")

    def test_shows_privacy_page(self):
        self.create_page(Page.PageType.PRIVACY)

        response = self.client.get(reverse("core:privacy"))

        self.assertEqual(
            response.context["page"].page_type,
            Page.PageType.PRIVACY,
        )

    def test_contains_correct_breadcrumbs(self):
        response = self.client.get(reverse("core:privacy"))

        self.assertListEqual(
            response.context["breadcrumbs"],
            [
                {
                    "title": "Home",
                    "url": reverse("core:home"),
                },
                {
                    "title": "Privacy Policy",
                },
            ],
        )
