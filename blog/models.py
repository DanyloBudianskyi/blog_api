from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.utils import timezone

# Create your models here.
class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_posts_count(self):
        return self.posts.count()

    def __str__(self):
        return self.username
    
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Користувач"
        verbose_name_plural = "Користувачі"
    
class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"
    
class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
    
class Post(models.Model):
    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published"),
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="posts")
    content = models.TextField()
    excerpt = models.TextField(blank=True, null=True)
    featured_image = models.ImageField(upload_to="posts/", blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    views_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name="posts")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        if self.status == "published" and not self.published_at:
            self.published_at = timezone.now()

        super().save(*args, **kwargs)

    def get_comments_count(self):
        return self.comments.filter(is_approved=True).count()

    def get_reading_time(self):
        words = len(self.content.split())
        return max(1, words // 200)
    
    def __str__(self):
        return self.title
            
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Пост"
        verbose_name_plural = "Пости"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies"
    )
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"
    
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Коментар"
        verbose_name_plural = "Коментарі"