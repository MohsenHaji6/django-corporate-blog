from django.test import RequestFactory
from django.urls import reverse

from blog.models import Article, Tag
from blog.tests.base import BaseBlogTest
from core.services.search import search


class SearchTest(BaseBlogTest):
    def test_query_less_than_3(self):
        request = RequestFactory().get(reverse("core:search"))
        self.assertEqual(search("te", request), [])

    def test_omit_word_length_less_than_3(self):
        request = RequestFactory().get(reverse("core:search"))
        self.assertEqual(search("te gh e 1 99", request), [])

    def test_pagination_search_results_by_15(self):
        request = RequestFactory().get(reverse("core:search") + "?page=2")
        for i in range(16):
            self.create_article(title=f"test {i}", status=Article.Status.PUBLISHED)

        results = search("test", request)

        self.assertEqual(results.number, 2)  # type: ignore
        self.assertEqual(len(results), 1)

    def test_search_through_the_published_articles(self):
        request = RequestFactory().get(reverse("core:search") + "?page=1")
        for i in range(25):
            if i <= 1:
                self.create_article(title=f"test {i}", status=Article.Status.DRAFT)
            if i > 1 and i <= 3:
                self.create_article(title=f"test {i}", status=Article.Status.ARCHIVED)
            if i > 3 and i <= 9:
                self.create_article(title=f"test {i}", status=Article.Status.SCHEDULED)
            if i > 9:
                self.create_article(title=f"test {i}", status=Article.Status.PUBLISHED)

        results = search("test", request)

        self.assertEqual(len(results), 15)
        for article in results:
            self.assertEqual(article.status, Article.Status.PUBLISHED)

    def test_title_score_must_be_10(self):
        request = RequestFactory().get(reverse("core:search"))
        self.create_article(title="score", status=Article.Status.PUBLISHED)

        score = search("score", request).object_list.values_list(  # type: ignore
            "search_score", flat=True
        )[0]
        self.assertEqual(score, 10)

    def test_content_score_must_be_5(self):

        request = RequestFactory().get(reverse("core:search"))
        self.create_article(content="score", status=Article.Status.PUBLISHED)

        score = search("score", request).object_list.values_list(  # type: ignore
            "search_score", flat=True
        )[0]
        self.assertEqual(score, 5)

    def test_tag_score_must_be_3(self):
        request = RequestFactory().get(reverse("core:search"))
        tag = Tag.objects.create(name="score")
        self.create_article(tags=tag, status=Article.Status.PUBLISHED)

        score = search("score", request).object_list.values_list(  # type: ignore
            "search_score", flat=True
        )[0]
        self.assertEqual(score, 3)

    def test_category_score_must_be_2(self):
        request = RequestFactory().get(reverse("core:search"))
        category = self.create_category_depth_3(root_name="score")["root"]
        self.create_article(
            title="test 3", category_main=category, status=Article.Status.PUBLISHED
        )
        score = search("score", request).object_list.values_list(  # type: ignore
            "search_score", flat=True
        )[0]
        self.assertEqual(score, 2)

    def test_ordering_by_score(self):
        request = RequestFactory().get(reverse("core:search"))

        self.create_article(title="test 0", status=Article.Status.PUBLISHED)

        self.create_article(title="test 1 score", status=Article.Status.PUBLISHED)

        self.create_article(
            title="test 2", content="score", status=Article.Status.PUBLISHED
        )

        category = self.create_category_depth_3(root_name="score")["root"]
        self.create_article(
            title="test 3", category_main=category, status=Article.Status.PUBLISHED
        )

        tag = Tag.objects.create(name="score")
        self.create_article(title="test 4", tags=tag, status=Article.Status.PUBLISHED)

        results = search("score", request)

        self.assertEqual(
            list(results.object_list.values_list("title", flat=True)),  # type: ignore
            ["test 1 score", "test 2", "test 4", "test 3"],
        )
