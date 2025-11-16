from rest_framework import serializers
from ..models import User, Category, Tag, Post, Comment

class UserSerializer(serializers.ModelSerializer):
    posts_count = serializers.IntegerField(source="get_posts_count", read_only=True)
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "bio",
            "avatar",
            "posts_count",
        ]

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()
    
    def validate_email(self, value):
        user = self.instance
        if user and user.email == value:
            return value
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пошта має бути унікальною")
        return value


class CategorySerializer(serializers.ModelSerializer):
    posts_count = serializers.IntegerField(source="posts.count", read_only=True)

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "description", "posts_count"]



class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name", "slug"]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ["id", "author", "content", "replies", "created_at"]

    def get_replies(self, obj):
        return CommentSerializer(obj.replies.all(), many=True).data

class PostListSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            "id", "title", "slug",
            "excerpt", "author", 
            "category", "tags",
            "views_count", "published_at",
        ]

class PostDetailSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    tags = TagSerializer(many=True, read_only=True)
    comments = serializers.SerializerMethodField()
    reading_time = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id", "title", "slug", "excerpt", "content",
            "author", "category", "tags",
            "reading_time", "comments_count", "comments",
            "views_count", "published_at"
        ]

    def get_comments(self, obj):
        qs = obj.comments.filter(parent=None)
        return CommentSerializer(qs, many=True).data
    
    def get_reading_time(self, obj):
        return obj.get_reading_time()

    def get_comments_count(self, obj):
        return obj.get_comments_count()
