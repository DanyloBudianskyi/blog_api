from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.db.models import Count, Sum, Avg
from rest_framework.response import Response

from .models import User, Category, Post, Tag
from blog.serializers.serializers import CategorySerializer, PostListSerializer, PostDetailSerializer, LikeSerializer
from blog.serializers.statistics import BlogStatisticsSerializer, CategoryStatisticsSerializer, TopPostSerializer, TopAuthorSerializer
# Create your views here.

#Пости
class PostListCreateApiView(generics.ListCreateAPIView):
    queryset = Post.objects.filter(status='published').select_related('author', 'category').prefetch_related('tags')
    serializer_class = PostListSerializer

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == "POST":
            self.permission_classes = [IsAdminUser]

        return super().get_permissions()

class MyPostListApiView(generics.ListAPIView):
    serializer_class = PostListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(author=user).select_related('author', 'category').prefetch_related('tags')
        
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostDetailDeleteUpdateApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.select_related('author', 'category').prefetch_related('tags', 'comments__author', 'comments__replies__author')
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'post_slug'

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method in ['PUT', 'DELETE', 'PATCH']:
            self.permission_classes = [IsAdminUser]

        return super().get_permissions()
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views_count += 1
        instance.save(update_fields=["views_count"])
        return super().retrieve(request, *args, **kwargs)


#Категорії
class CategoryListCreateApiView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == "POST":
            self.permission_classes = [IsAdminUser]

        return super().get_permissions()
    
class CategoryDetailDeleteUpdateApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.select_related().prefetch_related()
    serializer_class = CategorySerializer
    lookup_url_kwarg = 'category_id'

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method in ['PUT', 'DELETE', 'PATCH']:
            self.permission_classes = [IsAdminUser]

        return super().get_permissions()

class CategoryPostsAPIView(generics.ListAPIView):
    serializer_class = PostListSerializer

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        return Post.objects.filter(
            category__slug=category_slug,
            status='published'
        ).select_related('author', 'category').prefetch_related('tags')


class TagPostsAPIView(generics.ListAPIView):
    serializer_class = PostListSerializer

    def get_queryset(self):
        tag_slug = self.kwargs['tag_slug']
        return Post.objects.filter(
            tags__slug=tag_slug,
            status='published'
        ).select_related('author', 'category').prefetch_related('tags')

#Лайки
class PostLikesListAPIView(generics.ListAPIView):
    serializer_class = LikeSerializer

    def get_queryset(self):
        post = Post.objects.get(slug=self.kwargs['slug'])
        return post.likes.all()

class PostLikesCountAPIView(APIView):
    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        return Response({"likes_count": post.likes.count()})

#Закладки
class MyBookmarksAPIView(generics.ListAPIView):
    serializer_class = PostListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(bookmarks__user=self.request.user).distinct()

class PostBookmarksCountAPIView(APIView):
    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        return Response({"bookmarks_count": post.bookmarks.count()})

# Статистика
class BlogStatisticsAPIView(APIView):
    def get(self, request):
        total_posts = Post.objects.count()
        published_posts = Post.objects.filter(status="published").count()
        draft_posts = Post.objects.filter(status="draft").count()
        total_comments = Post.objects.aggregate(total_comments=Count("comments"))["total_comments"]
        total_views = Post.objects.aggregate(total_views=Sum("views_count"))["total_views"] or 0

        top_posts_qs = Post.objects.filter(status="published").order_by("-views_count")[:5]
        top_posts = TopPostSerializer(top_posts_qs, many=True).data

        top_authors_qs = User.objects.annotate(posts_count=Count("posts")).order_by("-posts_count")[:3]
        top_authors = TopAuthorSerializer(top_authors_qs, many=True).data

        data = {
            "total_posts": total_posts,
            "published_posts": published_posts,
            "draft_posts": draft_posts,
            "total_comments": total_comments,
            "total_views": total_views,
            "top_posts": top_posts,
            "top_authors": top_authors,
        }

        serializer = BlogStatisticsSerializer(data)
        return Response(serializer.data)


class CategoryStatisticsAPIView(APIView):
    def get(self, request):
        categories = Category.objects.annotate(
            posts_count=Count("posts"),
            total_views=Sum("posts__views_count")
        )

        data = []
        for cat in categories:
            posts = cat.posts.all().annotate(comments_count=Count("comments"))
            if posts:
                avg_comments = sum(p.comments_count for p in posts) / posts.count()
            else:
                avg_comments = 0

            data.append({
                "name": cat.name,
                "posts_count": cat.posts_count,
                "total_views": cat.total_views or 0,
                "avg_comments": avg_comments,
            })

        serializer = CategoryStatisticsSerializer(data, many=True)
        return Response(serializer.data)