from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Category, Tag, Post, Comment, Like, Bookmark

# Register your models here.
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Additional Info", {"fields": ("bio", "avatar")}),
    )

    list_display = ("username", "email", "first_name", "last_name", "created_at")
    search_fields = ("username", "email", "first_name", "last_name")
    list_filter = ("is_active", "is_staff", "is_superuser", "created_at")

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_at")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ("created_at",)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}

class LikeInline(admin.TabularInline):
    model = Like
    extra = 0
    autocomplete_fields = ("user",)
    readonly_fields = ("created_at",)

class BookmarkInline(admin.TabularInline):
    model = Bookmark
    extra = 0
    autocomplete_fields = ("user",)
    readonly_fields = ("created_at",)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "category", "status", "views_count", "created_at")
    list_filter = ("status", "category", "tags", "created_at")
    search_fields = ("title", "content", "author__username")
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ("author", "category", "tags")
    inlines = [LikeInline, BookmarkInline]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "post", "is_approved", "created_at")
    list_filter = ("is_approved", "created_at")
    search_fields = ("content", "author__username", "post__title")
    autocomplete_fields = ("author", "post", "parent")