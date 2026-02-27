from rest_framework import serializers

from posts.models import PostMedia, Post, Comment


class PostMediaSerializer(serializers.ModelSerializer):
    # Serializer for individual media files (image/video)

    class Meta:
        model = PostMedia
        fields = ['id', 'media_type', 'file', 'created_at']
        read_only_fields = ['id', 'created_at']

class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    # author_email = serializers.EmailField(source='author.email', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'author_name', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'author_name', 'created_at', 'updated_at']

class PostSerializer(serializers.ModelSerializer):
    # Main Post serializer with nested media and engagement counters.

    # Nested media (read-only)
    media = PostMediaSerializer(many=True, read_only=True)

    # Nested comments (read-only)
    comments = CommentSerializer(many=True, read_only=True)

    # Author metadata
    author_name = serializers.CharField(source='author.username', read_only=True)
    author_email = serializers.EmailField(source='author.email', read_only=True)

    # Engagement counters
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            'author',
            'author_name',
            'author_email',
            'content',
            'visibility',
            'media',
            'likes_count',
            'comments_count',
            'comments',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'author', 'likes_count', 'comments_count', 'comments', 'created_at', 'updated_at']

    def get_likes_count(self, obj):
        # Returns number of likes.
        return obj.likes.count()

    def get_comments_count(self, obj):
        # Returns number of comments.
        return obj.comments.count()

    def validate(self, data):
        # Ensure post is not completely empty. Must contain text OR media.

        request = self.context.get('request')
        content = data.get('content')
        files_exist = request.FILES if request else None

        if not content and not files_exist:
            raise serializers.ValidationError(
                "Post must contain text or at least one media file."
            )

        return data