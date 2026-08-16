from django.template import Context
from django.test import RequestFactory, SimpleTestCase

from core.templatetags.pagination_tags import query_transform


class QueryTransformTest(SimpleTestCase):
    def test_adds_page_parameter_and_preserves_existing_parameters(self):
        request = RequestFactory().get("/search/?q=django&category=python")

        context = Context({"request": request})

        result = query_transform(context, 2)

        self.assertEqual(
            result,
            "q=django&category=python&page=2",
        )

    def test_replaces_existing_page_parameter(self):
        request = RequestFactory().get("/search/?q=django&page=1")

        context = Context({"request": request})

        result = query_transform(context, 3)

        self.assertEqual(
            result,
            "q=django&page=3",
        )
