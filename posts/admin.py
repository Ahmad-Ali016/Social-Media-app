from django.contrib import admin
from posts.models import PostMedia, Post

# Register your models here.

class PostMediaInline(admin.TabularInline):

    # Allows viewing and editing media directly inside Post admin.

    model = PostMedia
    extra = 0
    readonly_fields = ['created_at']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    # Custom admin configuration for Post model.

    list_display = ['id', 'author', 'visibility', 'created_at']
    list_filter = ['visibility', 'created_at']
    search_fields = ['author__username', 'author__email', 'content']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [PostMediaInline]


@admin.register(PostMedia)
class PostMediaAdmin(admin.ModelAdmin):

    # Admin configuration for PostMedia model.

    list_display = ['id', 'post', 'media_type', 'created_at']
    list_filter = ['media_type', 'created_at']
    search_fields = ['post__author__username']
    readonly_fields = ['created_at']