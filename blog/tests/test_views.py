from django.urls import reverse

from blog.models import Article, Category, Comment, Tag

from .base import BaseBlogTest


class BlogListViewTest(BaseBlogTest):
    def test_returns_status_code_200(self):
        response = self.client.get(reverse("blog:list"))
        self.assertEqual(response.status_code, 200)

    def test_shows_only_published_articles(self):
        for i, status in enumerate(
            [
                Article.Status.PUBLISHED,
                Article.Status.DRAFT,
                Article.Status.ARCHIVED,
                Article.Status.SCHEDULED,
            ]
        ):
            self.create_article(title=f"test {i}", status=status)

        response = self.client.get(reverse("blog:list"))
        articles = response.context["articles"]
        self.assertTrue(articles)
        for article in articles:
            self.assertEqual(article.status, Article.Status.PUBLISHED)

    def test_paginates_articles_by_15(self):

        for i in range(16):
            self.create_article(title=f"test article {i}", status=Article.Status.PUBLISHED)

        response = self.client.get(reverse("blog:list"))
        self.assertEqual(len(response.context["articles"]), 15)

        response = self.client.get(reverse("blog:list"), {"page": 2})
        self.assertEqual(len(response.context["articles"]), 1)

    def test_uses_correct_template(self):
        response = self.client.get(reverse("blog:list"))
        self.assertTemplateUsed(response, "blog/blog_list.html")


class BlogCategoryListViewTest(BaseBlogTest):
    def test_returns_status_code_200(self):
        response = self.client.get(self.get_category_url())
        self.assertEqual(response.status_code, 200)

    def test_returns_status_code_404(self):
        response = self.client.get("/blog/cat/404/")
        self.assertEqual(response.status_code, 404)

    def test_shows_just_articles_of_category_a_not_category_b(self):
        category_a = Category.add_root(name="category a")
        article_1 = self.create_article(
            title="test 1", category_main=category_a, status=Article.Status.PUBLISHED
        )

        category_b = Category.add_root(name="category b")
        article_2 = self.create_article(
            title="test 2", category_main=category_b, status=Article.Status.PUBLISHED
        )

        response = self.client.get(self.get_category_url(slug=category_a.slug))
        articles = response.context["articles"]

        self.assertIn(article_1, articles)
        self.assertNotIn(article_2, articles)

    def test_shows_only_published_articles(self):
        for i, status in enumerate(
            [
                Article.Status.PUBLISHED,
                Article.Status.DRAFT,
                Article.Status.ARCHIVED,
                Article.Status.SCHEDULED,
            ]
        ):
            self.create_article(title=f"test {i}", status=status)

        response = self.client.get(self.get_category_url())
        articles = response.context["articles"]
        self.assertTrue(articles)
        for article in articles:
            self.assertEqual(article.status, Article.Status.PUBLISHED)

    def test_uses_correct_template(self):
        response = self.client.get(self.get_category_url())
        self.assertTemplateUsed(response, "blog/blog_list.html")

    def test_paginates_articles_by_15(self):
        for i in range(16):
            self.create_article(title=f"test article {i}", status=Article.Status.PUBLISHED)

        response = self.client.get(self.get_category_url())
        self.assertEqual(len(response.context["articles"]), 15)

        response = self.client.get(self.get_category_url(), {"page": 2})
        self.assertEqual(len(response.context["articles"]), 1)

    def test_get_category_ancestors(self):
        category_child = self.category.add_child(
            name="test category child",
        )
        category_sub_child = category_child.add_child(
            name="test category sub child",
        )
        response = self.client.get(self.get_category_url(slug=category_sub_child.slug))

        self.assertListEqual(
            response.context["open_category_ids"],
            [self.category.id, category_child.id, category_sub_child.id],
        )


class BlogTagListViewTest(BaseBlogTest):
    def test_returns_status_code_200(self):
        response = self.client.get(self.get_tag_url())
        self.assertEqual(response.status_code, 200)

    def test_returns_status_code_404(self):
        response = self.client.get("/blog/tag/404/")
        self.assertEqual(response.status_code, 404)

    def test_shows_just_articles_of_tag_a_not_tag_b(self):
        tag_a = Tag.objects.create(name="tag a")
        article_1 = self.create_article(
            title="test 1", tags=tag_a, status=Article.Status.PUBLISHED
        )

        tag_b = Tag.objects.create(name="tag b")
        article_2 = self.create_article(
            title="test 2", tags=tag_b, status=Article.Status.PUBLISHED
        )

        response = self.client.get(self.get_tag_url(slug=tag_a.slug))
        articles = response.context["articles"]

        self.assertIn(article_1, articles)
        self.assertNotIn(article_2, articles)

    def test_uses_correct_template(self):
        response = self.client.get(self.get_tag_url())
        self.assertTemplateUsed(response, "blog/blog_list.html")

    def test_shows_only_published_articles(self):
        for i, status in enumerate(
            [
                Article.Status.PUBLISHED,
                Article.Status.DRAFT,
                Article.Status.ARCHIVED,
                Article.Status.SCHEDULED,
            ]
        ):
            self.create_article(title=f"test {i}", status=status)

        response = self.client.get(self.get_tag_url())
        articles = response.context["articles"]
        self.assertTrue(articles)
        for article in articles:
            self.assertEqual(article.status, Article.Status.PUBLISHED)

    def test_paginates_articles_by_15(self):
        for i in range(16):
            self.create_article(title=f"test article {i}", status=Article.Status.PUBLISHED)

        response = self.client.get(self.get_tag_url())
        self.assertEqual(len(response.context["articles"]), 15)

        response = self.client.get(self.get_tag_url(), {"page": 2})
        self.assertEqual(len(response.context["articles"]), 1)


class BlogDetailViewTest(BaseBlogTest):
    def test_returns_status_code_200(self):
        response = self.client.get(self.get_article_url())
        self.assertEqual(response.status_code, 200)

    def test_returns_status_code_404(self):
        response = self.client.get("/blog/404/")
        self.assertEqual(response.status_code, 404)

    def test_uses_correct_template(self):
        response = self.client.get(self.get_article_url())
        self.assertTemplateUsed(response, "blog/blog_detail.html")

    def test_shows_only_approved_comments(self):
        article = self.create_article(status=Article.Status.PUBLISHED)
        for i, status in enumerate(
            [Comment.Status.APPROVED, Comment.Status.PENDING, Comment.Status.SPAM]
        ):
            Comment.objects.create(
                article=article,
                name=f"test name{i}",
                email=f"test{i}@email.com",
                body=f"test body comment {i}",
                status=status,
            )

        response = self.client.get(self.get_article_url(slug=article.slug))
        comments = response.context["page_comments"]

        for comment in comments:
            self.assertEqual(comment.status, Comment.Status.APPROVED)

    def test_pagination_comments_by_10(self):
        article = self.create_article(status=Article.Status.PUBLISHED)
        for i in range(11):
            Comment.objects.create(
                article=article,
                name=f"test name{i}",
                email=f"test{i}@email.com",
                body=f"test body comment {i}",
                status=Comment.Status.APPROVED,
            )

        response = self.client.get(self.get_article_url(slug=article.slug))
        self.assertEqual(len(response.context["page_comments"]), 10)

        response = self.client.get(self.get_article_url(slug=article.slug), {"page": 2})
        self.assertEqual(len(response.context["page_comments"]), 1)

    def test_comment_form_valid(self):
        response = self.client.post(
            self.get_article_url(),
            data={"name": "test", "email": "test@email.com", "body": "test body"},
        )
        comment = Comment.objects.first()
        self.assertEqual(comment.status, Comment.Status.PENDING)  # type: ignore
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), 1)

    def test_comment_form_invalid(self):
        response = self.client.post(
            self.get_article_url(),
            data={"name": "", "email": "", "body": ""},
        )

        form = response.context["form"]

        self.assertIn("name", form.errors)
        self.assertIn("email", form.errors)
        self.assertIn("body", form.errors)

        self.assertEqual(Comment.objects.count(), 0)
