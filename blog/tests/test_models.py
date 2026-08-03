from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from blog.models import Article, Category, Comment, Tag


class CategoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.category = Category.objects.create(name="test category", depth=1)

    def test_str(self):
        self.assertEqual(str(self.category), "test category")

    def test_slug_is_generated_on_save(self):
        self.assertEqual(self.category.slug, "test-category")

    def test_get_absolute_url(self):
        self.assertEqual(
            self.category.get_absolute_url(),
            reverse("blog:category", kwargs={"slug": self.category.slug}),
        )


class TagModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.tag = Tag.objects.create(name="test tag")

    def test_str(self):
        self.assertEqual(str(self.tag), "test tag")

    def test_slug_is_generated_on_save(self):
        self.assertEqual(self.tag.slug, "test-tag")

    def test_get_absolute_url(self):
        self.assertEqual(
            self.tag.get_absolute_url(),
            reverse("blog:tag", kwargs={"slug": self.tag.slug}),
        )


class ArticleModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.article = Article.objects.create(
            title="test title article",
            author=get_user_model().objects.create_user(phone_number="09123456789"),  # type: ignore
            content="test content article",
            image="test.jpg",
            image_alt_text="test",
            category_main=Category.objects.create(name="test category", depth=1),
        )

    def test_str(self):
        self.assertEqual(str(self.article), "test title article")

    def test_slug_is_generated_on_save(self):
        self.assertEqual(self.article.slug, "test-title-article")

    def test_get_absolute_url(self):
        self.assertEqual(
            self.article.get_absolute_url(),
            reverse("blog:detail", kwargs={"slug": self.article.slug}),
        )

    def test_status_default(self):
        self.assertEqual(self.article.status, Article.Status.DRAFT)


class CommentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.comment = Comment.objects.create(
            article=Article.objects.create(
                title="test title article",
                author=get_user_model().objects.create_user(phone_number="09123456789"),  # type: ignore
                content="test content article",
                image="test.jpg",
                image_alt_text="test",
                category_main=Category.objects.create(name="test category", depth=1),
            ),
            name="test name",
            email="test@mail.com",
            body="test body",
        )

    def test_status_default(self):
        self.assertEqual(self.comment.status, Comment.Status.PENDING)
