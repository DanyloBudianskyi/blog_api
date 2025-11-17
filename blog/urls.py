from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('posts/', views.PostListCreateApiView.as_view(), name="post_list"),
    path('my-post/', views.MyPostListApiView.as_view(), name="my_post_list"),
    path('posts/<slug:post_slug>/', views.PostDetailDeleteUpdateApiView.as_view(), name="post_detail"),
    
    path('categories/', views.CategoryListCreateApiView.as_view(), name="category_list"),
    path('categories/<int:category_id>/', views.CategoryDetailDeleteUpdateApiView.as_view(), name="category_detail"),
    path('categories/<slug:category_slug>/', views.CategoryPostsAPIView.as_view(), name='category_posts'),
    
    path('tag/<slug:tag_slug>/', views.TagPostsAPIView.as_view(), name='tag_posts'),
    
    path("posts/<slug:slug>/likes/", views.PostLikesListAPIView.as_view(), name='post_likes'),
    path("posts/<slug:slug>/likes-count/", views.PostLikesCountAPIView.as_view(), name='post_likes_count'),
    
    path("my-bookmarks/", views.MyBookmarksAPIView.as_view(), name='my_bookmarks'),
    path("posts/<slug:slug>/bookmarks-count/", views.PostBookmarksCountAPIView.as_view(), name='post_bookmarks_count'),
    
    path("statistics/blog/", views.BlogStatisticsAPIView.as_view(), name="blog-statistics"),
    path("statistics/categories/", views.CategoryStatisticsAPIView.as_view(), name="category-statistics"),

    path("authors/", views.AuthorsListAPIView.as_view(), name="authors_list"),
    path("authors/top/", views.TopAuthorsAPIView.as_view(), name="top_authors"),
    path("authors/<int:id>/", views.AuthorDetailAPIView.as_view(), name="author_detail"),
    path("authors/<int:id>/posts/", views.AuthorPostsAPIView.as_view(), name="author_posts"),
    path("authors/<int:id>/followers/", views.AuthorFollowersAPIView.as_view(), name="author_followers"),
    path("authors/<int:id>/stats/", views.AuthorStatsAPIView.as_view(), name="author_stats"),
]
