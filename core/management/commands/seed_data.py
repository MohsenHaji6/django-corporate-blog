import random
from decimal import Decimal

from django.apps import apps
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import connection, transaction
from django.utils.text import slugify
from faker import Faker

User = get_user_model()
fake = Faker()


class Command(BaseCommand):
    help = "Generate fake data for all of apps"

    def add_arguments(self, parser):
        # parser.add_argument("--users", type=int, default=10, help="Number of users")
        parser.add_argument(
            "--clean",
            action="store_true",
            help="Cleaning previous data before generating new data",
        )

    def handle(self, *args, **options):
        # user_count = options["users"]
        clean = options["clean"]

        if clean:
            self.clean_all_data()

        self.stdout.write(
            self.style.NOTICE("All previous data was deleted from the database!")
        )
        self.stdout.write(self.style.SUCCESS("Start generate fake data..."))

        with transaction.atomic():
            # self.create_users(user_count)

            for model in apps.get_models():
                app_label = model._meta.app_label
                model_name = model.__name__

                if app_label in ["admin", "auth", "contenttypes", "sessions"]:
                    continue

                self.stdout.write(f"In generation for: {app_label}.{model_name}")

                self.generate_data_for_model(model)

        self.stdout.write(self.style.SUCCESS("Generate data was successful"))

    def clean_all_data(self):
        self.stdout.write("Cleaning previous data...")

        with connection.cursor() as cursor:
            cursor.execute("SET session_replication_role = 'replica';")

            # 1. backup superuser
            cursor.execute("""
                CREATE TEMP TABLE superusers_backup AS 
                SELECT * FROM accounts_customuser WHERE is_superuser = true;
            """)

            # 2. Get all tables
            cursor.execute("""
                SELECT tablename FROM pg_tables 
                WHERE schemaname = 'public'
                AND tablename NOT IN (
                    'django_content_type',
                    'django_session',
                    'django_migrations'
                );
            """)

            tables = [row[0] for row in cursor.fetchall()]

            # 3. Truncate all tables
            for table in tables:
                try:
                    cursor.execute(f'TRUNCATE TABLE "{table}" RESTART IDENTITY CASCADE;')
                    self.stdout.write(f"✓ Truncated {table}")
                except Exception as e:
                    self.stdout.write(f"✗ Error truncating {table}: {e}")

            # 4. Restore data
            cursor.execute(
                "INSERT INTO accounts_customuser SELECT * FROM superusers_backup;"
            )

            # 5. Reset sequences
            for table_name in [
                "accounts_customuser",
            ]:
                cursor.execute(f"""
                    SELECT setval('{table_name}_id_seq', 
                        (SELECT COALESCE(MAX(id), 0) FROM {table_name}));
                """)

            # 7. Cleanup
            cursor.execute("DROP TABLE IF EXISTS superusers_backup;")
            cursor.execute("SET session_replication_role = 'origin';")

        self.stdout.write(
            self.style.SUCCESS("✓ Done! Superusers and location data preserved!")
        )

    # def create_users(self, count):

    #     self.stdout.write(f"Create user {count} ...")

    #     for i in range(count):
    #         while True:
    #             phone_number = f"09{random.randint(100000000, 999999999)}"
    #             if not User.objects.filter(phone_number=phone_number).exists():
    #                 break
    #         user, created = User.objects.get_or_create(
    #             phone_number=phone_number,
    #             defaults={
    #                 "email": fake.unique.email(),
    #                 "first_name": fake.first_name(),
    #                 "last_name": fake.last_name(),
    #                 "is_staff": fake.boolean(chance_of_getting_true=10),
    #             },
    #         )
    #         if created:
    #             user.set_password("pass123")
    #             user.save()

    def generate_data_for_model(self, model):
        """Generating data for a specific model using its structure"""

        model_name = model.__name__

        if model_name == "Category":
            self.create_categories(model)
        elif model_name == "Tag":
            self.create_tags(model)
        elif model_name == "Article":
            self.create_articles(model)
        elif model_name == "Comment":
            self.create_comments(model)
        elif model_name == "Product":
            self.create_products(model)
        elif model_name == "ProductVariant":
            self.create_product_variants(model)

    def create_categories(self, Category):
        parents = [f"category parent {i}" for i in range(5)]
        children = [f"category child {i}" for i in range(15)]
        sub_children = [f"category sub child {i}" for i in range(30)]

        # Create parents
        parent_nodes = []
        for name in parents:
            parent = Category.add_root(
                name=name,
                slug=slugify(name, allow_unicode=True),
                description=fake.paragraph(nb_sentences=2),
                meta_title=name,
                meta_description=fake.sentence(nb_words=18),
            )
            parent_nodes.append(parent)

        # Create children and connect to parents
        child_nodes = []
        for i, name in enumerate(children):
            parent = parent_nodes[i % len(parent_nodes)]

            child = parent.add_child(
                name=name,
                slug=slugify(name, allow_unicode=True),
                description=fake.paragraph(nb_sentences=2),
                meta_title=name,
                meta_description=fake.sentence(nb_words=18),
            )
            child_nodes.append(child)

        # Create sub children and connect to children
        for i, name in enumerate(sub_children):
            child = child_nodes[i % len(child_nodes)]

            child.add_child(
                name=name,
                slug=slugify(name, allow_unicode=True),
                description=fake.paragraph(nb_sentences=2),
                meta_title=name,
                meta_description=fake.sentence(nb_words=18),
            )

    def create_tags(self, Tag):
        tags = [f"tag {i}" for i in range(30)]
        for name in tags:
            Tag.objects.get_or_create(
                name=name,
                slug=name,
                meta_title=name,
                meta_description=fake.sentence(nb_words=18),
            )

    def create_articles(self, Article):
        User = apps.get_model("accounts", "CustomUser")
        Category = apps.get_model("blog", "Category")
        Tag = apps.get_model("blog", "Tag")

        # Just superuser
        user = User.objects.filter(is_superuser=True).first()

        if not user:
            self.stdout.write(self.style.ERROR("No superuser found."))
            return

        categories = list(Category.objects.all())
        tags = list(Tag.objects.all())

        for i in range(100):
            title = fake.sentence(nb_words=5).rstrip(".")

            # Create slug from unique title
            slug = f"{slugify(title, allow_unicode=True)}-{random.randint(1000, 9999)}"

            article = Article.objects.create(
                title=title,
                slug=slug,
                author=user,
                content="\n".join(fake.paragraphs(nb=3)),
                summary=fake.sentence(nb_words=30),
                meta_title=title,
                meta_description=fake.text(max_nb_chars=160),
                image=f"blog/{random.randint(1, 20)}.jpg",
                image_alt_text=fake.text(max_nb_chars=20),
                published_at=fake.date_time_between(start_date="-3y", end_date="now"),
                status=Article.Status.PUBLISHED,
                category_main=random.choice(categories),
            )

            # choice 3 to 5 tags for every article
            selected_tags = random.sample(tags, k=random.randint(3, 5))
            article.tags.set(selected_tags)

        self.stdout.write(self.style.SUCCESS("500 articles created successfully."))

    def create_comments(self, Comment):
        Article = apps.get_model("blog", "Article")

        # Get the last 10 articles based on publication date
        articles = Article.objects.order_by("-published_at")[:10]

        if not articles:
            self.stdout.write(self.style.ERROR("No articles found."))
            return

        total_comments = 0

        for article in articles:
            # Comment number between 3 to 20 for every articles
            comments_count = random.randint(3, 20)

            for _ in range(comments_count):
                # Comment date should be after article publication date
                created_at = fake.date_time_between(
                    start_date=article.published_at,  # type: ignore
                    end_date="now",
                )

                Comment.objects.create(
                    article=article,
                    body=fake.paragraph(nb_sentences=2),
                    name=fake.name(),
                    email=fake.email(),
                    created_at=created_at,
                    status=Comment.Status.APPROVED,
                )

                total_comments += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"{total_comments} comments created for 10 latest articles."
            )
        )

    def create_products(self, Product):
        laptop_brands = [
            "Apple",
            "Dell",
            "HP",
            "Lenovo",
            "Asus",
            "Samsung",
            "Microsoft",
            "Fujitsu",
            "LG",
            "Sony",
        ]
        for i, name in enumerate(laptop_brands):
            Product.objects.create(name=name, order=i)

        self.stdout.write(self.style.SUCCESS("10 products created."))

    def create_product_variants(self, ProductVariant):
        Product = apps.get_model("catalog", "Product")

        laptop_models = {
            "Apple": [
                "MacBook Air M2",
                "MacBook Air M3",
                "MacBook Pro 14",
                "MacBook Pro 16",
            ],
            "Dell": ["XPS 13", "XPS 15", "Inspiron 14", "Latitude 5440"],
            "HP": ["Spectre x360", "Envy 13", "Pavilion 15", "EliteBook 840"],
            "Lenovo": ["ThinkPad X1 Carbon", "Yoga 7", "IdeaPad 5", "Legion 5"],
            "Asus": ["ZenBook 14", "VivoBook 15", "ROG Strix G15", "TUF Gaming A15"],
            "Samsung": ["Galaxy Book3", "Galaxy Book4", "Galaxy Book Pro"],
            "Microsoft": ["Surface Laptop 5", "Surface Laptop 6", "Surface Book 3"],
            "Fujitsu": ["LIFEBOOK U9311", "LIFEBOOK A3510"],
            "LG": ["Gram 14", "Gram 16", "Ultra PC"],
            "Sony": ["VAIO SX14", "VAIO Z", "VAIO FE14"],
        }

        feature_pool = [
            "Intel Core i5 Processor",
            "Intel Core i7 Processor",
            "AMD Ryzen 5 Processor",
            "AMD Ryzen 7 Processor",
            "8GB RAM",
            "16GB RAM",
            "32GB RAM",
            "256GB SSD",
            "512GB SSD",
            "1TB SSD",
            "13.3-inch Display",
            "14-inch Display",
            "15.6-inch Display",
            "17-inch Display",
            "Full HD Resolution",
            "2K Resolution",
            "4K Resolution",
            "Backlit Keyboard",
            "Fingerprint Reader",
            "Wi-Fi 6",
        ]

        for product in Product.objects.all()[:10]:
            variant_count = random.randint(1, 5)

            # Choice one brand for this product
            brand = random.choice(list(laptop_models.keys()))
            available_models = laptop_models[brand].copy()

            for order in range(variant_count):
                # Choosing a model without repetition as much as possible
                if available_models:
                    model = random.choice(available_models)
                    available_models.remove(model)
                else:
                    model = random.choice(laptop_models[brand])

                # Creating features with circular bullets
                selected_features = random.sample(feature_pool, k=random.randint(3, 5))
                features = "\n".join([f"• {feature}" for feature in selected_features])

                # Decimal price between $150 and $1200 with two decimal places
                price = Decimal(str(round(random.uniform(150, 1200), 2)))

                ProductVariant.objects.create(
                    product=product,
                    title=f"{brand} {model}",
                    features=features,
                    unit_price=price,
                    in_stock=random.choice([True, False]),
                    image=f"product/{random.randint(1, 20)}.jpg",
                    updated_at=fake.date_time_between(start_date="-2M", end_date="now"),
                    order=order + 1,
                )
