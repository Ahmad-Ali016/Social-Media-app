from rest_framework import serializers

from posts.models import PostMedia, Post


class PostMediaSerializer(serializers.ModelSerializer):

    # Serializer for individual media files (image/video)

    class Meta:
        model = PostMedia
        fields = ['id', 'media_type', 'file', 'created_at']
        read_only_fields = ['id', 'created_at']

class PostSerializer(serializers.ModelSerializer):

    # Main Post serializer with nested media support.

    # Nested media (read-only for now)
    media = PostMediaSerializer(many=True, read_only=True)

    # Author username
    author_name = serializers.CharField(source='author.username', read_only=True)
    # Author email
    author_email = serializers.EmailField(source='author.email', read_only=True)

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
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']

    def validate(self, data):

        # Ensure post is not completely empty. Must contain text OR media.

        request = self.context.get('request')
        content = data.get('content')
        files = request.FILES if request else None

        if not content and not files:
            raise serializers.ValidationError(
                "Post must contain text or at least one media file."
            )

        return data