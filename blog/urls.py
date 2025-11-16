from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('posts/', views.PostListCreateApiView.as_view(), name="post_list"),
    path('my-post/', views.MyPostListApiView.as_view(), name="my_post_list"),
    path('posts/<int:post_id>/', views.PostDetailDeleteUpdateApiView.as_view(), name="post_detail"),
    path('categories/', views.CategoryListCreateApiView.as_view(), name="category_list"),
    path('categories/<int:category_id>/', views.CategoryDetailDeleteUpdateApiView.as_view(), name="category_detail"),
    path('categories/<slug:category_slug>/', views.CategoryPostsAPIView.as_view(), name='category_posts'),
    path('tag/<slug:tag_slug>/', views.TagPostsAPIView.as_view(), name='tag_posts'),
    path("statistics/blog/", views.BlogStatisticsAPIView.as_view(), name="blog-statistics"),
    path("statistics/categories/", views.CategoryStatisticsAPIView.as_view(), name="category-statistics"),
]
