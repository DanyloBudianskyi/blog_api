import django_filters
from django.db.models import Count
from blog.models import Post

class PostFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name="category__slug", lookup_expr='iexact')
    tag = django_filters.CharFilter(field_name="tags__slug", lookup_expr='iexact')
    author = django_filters.CharFilter(field_name="author__username", lookup_expr='iexact')
    date_from = django_filters.DateFilter(field_name="created_at", lookup_expr="gte")
    date_to = django_filters.DateFilter(field_name="created_at", lookup_expr="lte")
    status = django_filters.CharFilter(field_name="status", lookup_expr='iexact')
    
    class Meta:
        model = Post
        fields = ["category", "tags", "author", "status", "created_at"]