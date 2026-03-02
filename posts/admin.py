from django.contrib import admin
from posts.models import PostMedia, Post, PostLike, Comment


# Register your models here.

# Inline for PostMedia (show media directly in Post admin)
class PostMediaInline(admin.TabularInline):

    # Allows viewing and editing media directly inside Post admin.

    model = PostMedia
    extra = 0
    readonly_fields = ['created_at']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    # Custom admin configuration for Post model.
    list_display = [
        'id',
        'author',
        'author_email',
        # 'content_snippet',
        'visibility',
        'likes_count',
        'comments_count',
        'created_at',
    ]
    list_filter = ['visibility', 'created_at']
    search_fields = ['author__username', 'author__email']
    readonly_fields = ['created_at', 'updated_at', 'likes_count', 'comments_count']
    inlines = [PostMediaInline]

    # # Show first 50 characters of content
    # def content_snippet(self, obj):
    #     return obj.content[:50] + ('...' if len(obj.content) > 50 else '')
    #
    # content_snippet.short_description = 'Content'

    # Likes count
    def likes_count(self, obj):
        return obj.likes.count()

    likes_count.short_description = 'Likes'

    # Comments count
    def comments_count(self, obj):
        return obj.comments.count()

    comments_count.short_description = 'Comments'

    # Optional: show author email
    def author_email(self, obj):
        return obj.author.email

    author_email.short_description = 'Author Email'

@admin.register(PostMedia)
class PostMediaAdmin(admin.ModelAdmin):

    # Admin configuration for PostMedia model.
    list_display = ['id', 'post', 'media_type', 'created_at']
    list_filter = ['media_type', 'created_at']
    search_fields = ['post__author__username']
    readonly_fields = ['created_at']

@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['post__author__username', 'user__username']
    readonly_fields = ['created_at']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'author', 'comment_number', 'content', 'created_at']
    search_fields = ['author__username', 'content', 'post__id']
    list_filter = ['created_at']
    readonly_fields = ['created_at', 'updated_at']