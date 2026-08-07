from django.urls import reverse

from blog.models import Article, Comment

from .base import BaseBlogTest


class CategoryModelTest(BaseBlogTest):
    def test_str(self):
        self.assertEqual(str(self.category), "test category")

    def test_slug_is_generated_on_save(self):
        self.assertEqual(self.category.slug, "test-category")

    def test_get_absolute_url(self):
        self.assertEqual(
            self.category.get_absolute_url(),
            reverse("blog:category", kwargs={"slug": self.category.slug}),
        )


class TagModelTest(BaseBlogTest):
    def test_str(self):
        self.assertEqual(str(self.tag), "test tag")

    def test_slug_is_generated_on_save(self):
        self.assertEqual(self.tag.slug, "test-tag")

    def test_get_absolute_url(self):
        self.assertEqual(
            self.tag.get_absolute_url(),
            reverse("blog:tag", kwargs={"slug": self.tag.slug}),
        )


class ArticleModelTest(BaseBlogTest):
    def test_str(self):
        self.assertEqual(str(self.create_article()), "test article")

    def test_slug_is_generated_on_save(self):
        self.assertEqual(self.create_article().slug, "test-article")

    def test_get_absolute_url(self):
        article = self.create_article()
        self.assertEqual(
            article.get_absolute_url(),
            reverse("blog:detail", kwargs={"slug": article.slug}),
        )

    def test_status_default(self):
        self.assertEqual(self.create_article().status, Article.Status.DRAFT)


class CommentModelTest(BaseBlogTest):
    def test_status_default(self):
        comment = Comment.objects.create(
            article=self.create_article(),
            name="test name",
            email="test@mail.com",
            body="test body",
        )
        self.assertEqual(comment.status, Comment.Status.PENDING)
