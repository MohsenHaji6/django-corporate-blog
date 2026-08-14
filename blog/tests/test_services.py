from datetime import date
from unittest.mock import patch

from django.test import Client

from blog.models import Article, ArticleView, Category
from blog.services import (
    build_article_breadcrumb,
    build_category_breadcrumb,
    build_category_tree,
)

from .base import BaseBlogTest


class ArticleViewsTest(BaseBlogTest):
    def test_does_not_increment_view_count_on_page_refresh(self):
        article = self.create_article(status=Article.Status.PUBLISHED)
        client1 = self.client
        client1.get(self.get_article_url(slug=article.slug))

        self.assertEqual(ArticleView.objects.count(), 1)

        article.refresh_from_db()
        self.assertEqual(article.views_count, 1)

        self.assertTrue(
            ArticleView.objects.filter(
                article=article,
                session_key=self.client.session.session_key,
            ).exists()
        )

        client1.get(self.get_article_url(slug=article.slug))

        self.assertEqual(ArticleView.objects.count(), 1)

        article.refresh_from_db()
        self.assertEqual(article.views_count, 1)

    @patch("blog.services.article_views.timezone.localdate")
    def test_register_article_view_different_days(self, mock_localdate):
        article = self.create_article(status=Article.Status.PUBLISHED)

        mock_localdate.return_value = date(2026, 8, 6)

        self.client.get(self.get_article_url(slug=article.slug))
        article.refresh_from_db()
        self.assertEqual(article.views_count, 1)

        mock_localdate.return_value = date(2026, 8, 7)

        self.client.get(self.get_article_url(slug=article.slug))
        article.refresh_from_db()
        self.assertEqual(ArticleView.objects.count(), 2)
        self.assertEqual(article.views_count, 2)

    def test_increment_view_count_with_different_sessions(self):
        article = self.create_article(status=Article.Status.PUBLISHED)
        client1 = Client()
        client2 = Client()

        client1.get(self.get_article_url(slug=article.slug))
        client2.get(self.get_article_url(slug=article.slug))

        self.assertNotEqual(client1.session.session_key, client2.session.session_key)
        self.assertEqual(ArticleView.objects.count(), 2)

        article.refresh_from_db()
        self.assertEqual(article.views_count, 2)


class BuildBreadcrumbTest(BaseBlogTest):
    def test_build_category_breadcrumb(self):
        child3 = self.create_category_depth_3()["child3"]
        categories = child3.get_ancestors()
        breadcrumbs = build_category_breadcrumb(child3, categories)

        instance_breadcrumbs = [
            {"title": "Home", "url": "/"},
            {"title": "Blog", "url": "/blog/"},
            {"title": "Test root 1", "url": "/blog/cat/test-root-1/"},
            {"title": "Test child 2", "url": "/blog/cat/test-child-2/"},
            {"title": "Test child 3"},
        ]

        self.assertListEqual(breadcrumbs, instance_breadcrumbs)

    def test_build_article_breadcrumb(self):
        child3 = self.create_category_depth_3()["child3"]
        article = self.create_article(category_main=child3)
        breadcrumbs = build_article_breadcrumb(article)

        instance_breadcrumbs = [
            {"title": "Home", "url": "/"},
            {"title": "Blog", "url": "/blog/"},
            {"title": "Test child 3", "url": "/blog/cat/test-child-3/"},
            {"title": "Test article"},
        ]

        self.assertListEqual(breadcrumbs, instance_breadcrumbs)


class CategoryTreeTest(BaseBlogTest):
    def test_build_category_tree(self):
        self.create_category_depth_3()
        instance_category_tree = [
            {
                "pk": 1,
                "name": "test category",
                "slug": "test-category",
                "depth": 1,
                "url": "/blog/cat/test-category/",
                "children": [],
            },
            {
                "pk": 2,
                "name": "test root 1",
                "slug": "test-root-1",
                "depth": 1,
                "url": "/blog/cat/test-root-1/",
                "children": [
                    {
                        "pk": 3,
                        "name": "test child 2",
                        "slug": "test-child-2",
                        "depth": 2,
                        "url": "/blog/cat/test-child-2/",
                        "children": [
                            {
                                "pk": 4,
                                "name": "test child 3",
                                "slug": "test-child-3",
                                "depth": 3,
                                "url": "/blog/cat/test-child-3/",
                                "children": [],
                            }
                        ],
                    }
                ],
            },
        ]

        self.assertListEqual(build_category_tree(), instance_category_tree)

    def test_build_category_tree_by_paths(self):
        for i in range(2):
            self.create_category_depth_3(
                root_name=f"root {i}",
                child_name=f"child {i}",
                sub_child_name=f"sub child {i}",
            )

        paths = [Category.objects.filter(depth=1).values_list("path", flat=True)]
        instance_category_tree = [
            {
                "pk": 2,
                "name": "root 0",
                "slug": "root-0",
                "depth": 1,
                "url": "/blog/cat/root-0/",
                "children": [],
            },
            {
                "pk": 5,
                "name": "root 1",
                "slug": "root-1",
                "depth": 1,
                "url": "/blog/cat/root-1/",
                "children": [],
            },
            {
                "pk": 1,
                "name": "test category",
                "slug": "test-category",
                "depth": 1,
                "url": "/blog/cat/test-category/",
                "children": [],
            },
        ]
        self.assertListEqual(instance_category_tree, build_category_tree(paths=paths))

        paths_1 = [Category.objects.get(name="root 0").path]
        instance_category_tree_1 = [
            {
                "pk": 2,
                "name": "root 0",
                "slug": "root-0",
                "depth": 1,
                "url": "/blog/cat/root-0/",
                "children": [],
            }
        ]
        self.assertListEqual(build_category_tree(paths_1), instance_category_tree_1)
