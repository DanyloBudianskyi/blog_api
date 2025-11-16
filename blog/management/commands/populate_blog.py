from django.core.management.base import BaseCommand
import random
from blog.models import User, Category, Tag, Post, Comment


class Command(BaseCommand):
    help = "Заповнення блогу"

    def handle(self, *args, **kwargs):
        
        Category.objects.all().delete()
        Tag.objects.all().delete()
        Post.objects.all().delete()
        Comment.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

        authors = []
        for i in range(3):
            user = User.objects.create_user(
                username=f"user{i + 1}",
                email=f"user{i + 1}@example.com",
                password="123456",
                bio=f'Біо користувача {i + 1}',
            )
            authors.append(user)

        self.stdout.write(self.style.SUCCESS("✔ Створено 3 автори"))

        categories = []
        for i in range(5):
            cat = Category.objects.create(
                name=f'Категорія {i + 1}',
                description=f'Категорія {i + 1}'
            )
            categories.append(cat)

        self.stdout.write(self.style.SUCCESS("✔ Створено 5 категорій"))

        tags = []
        for i in range(10):
            tag = Tag.objects.create(name=f'Тег {i + 1}')
            tags.append(tag)

        self.stdout.write(self.style.SUCCESS("✔ Створено 10 тегів"))


        posts = []
        for i in range(20):
            post = Post.objects.create(
                title=f'Назва {i + 1}',
                author=random.choice(authors),
                category=random.choice(categories),
                content=f'Контент {i + 1}',
                excerpt=f'Короткий опис {i + 1}',
                status="published",
                views_count=random.randint(0, 500),
            )

            post.tags.add(*random.sample(tags, random.randint(1, 5)))

            posts.append(post)

        self.stdout.write(self.style.SUCCESS("✔ Створено 20 постів"))

        for i in range(50):
            Comment.objects.create(
                post=random.choice(posts),
                author=random.choice(authors),
                content=f'Контент коментаря {i + 1}',
                is_approved=True,
                parent=None if random.random() > 0.3 else Comment.objects.order_by("?").first(),
            )

        self.stdout.write(self.style.SUCCESS("✔ Створено 50 коментарів"))
        self.stdout.write(self.style.SUCCESS("🎉 Blog populated successfully!"))
