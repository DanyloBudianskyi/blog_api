from rest_framework import serializers
from blog.models import Post, User

class TopPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "title", "views_count", "published_at"]


class TopAuthorSerializer(serializers.ModelSerializer):
    posts_count = serializers.IntegerField()

    class Meta:
        model = User
        fields = ["id", "username", "posts_count"]


class BlogStatisticsSerializer(serializers.Serializer):
    total_posts = serializers.IntegerField()
    published_posts = serializers.IntegerField()
    draft_posts = serializers.IntegerField()
    total_comments = serializers.IntegerField()
    total_views = serializers.IntegerField()
    top_posts = TopPostSerializer(many=True)
    top_authors = TopAuthorSerializer(many=True)


class CategoryStatisticsSerializer(serializers.Serializer):
    name = serializers.CharField()
    posts_count = serializers.IntegerField()
    total_views = serializers.IntegerField()
    avg_comments = serializers.FloatField()
