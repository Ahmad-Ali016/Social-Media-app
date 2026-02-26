from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

from posts.models import Post, PostMedia
from posts.serializers import PostSerializer
from friends.models import Friendship

# Create your views here.

class CreatePostView(APIView):

    # POST -> Create a new post
    # Supports: Text (optional), Multiple images/videos and Visibility selection

    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Extract text and visibility
        content = request.data.get('content')
        visibility = request.data.get('visibility', 'FRIENDS')

        # Get uploaded files (can be multiple)
        files = request.FILES.getlist('media')

        # Validate: must have text or media
        if not content and not files:
            return Response(
                {"error": "Post must contain text or at least one media file."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create Post instance
        post = Post.objects.create(
            author=request.user,
            content=content,
            visibility=visibility
        )

        # Create media objects if provided
        for file in files:
            # Determine media type automatically
            if file.content_type.startswith('image'):
                media_type = 'IMAGE'
            elif file.content_type.startswith('video'):
                media_type = 'VIDEO'
            else:
                post.delete()  # rollback if invalid file
                return Response(
                    {"error": "Only image and video files are allowed."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            PostMedia.objects.create(
                post=post,
                media_type=media_type,
                file=file
            )

        # Serialize and return created post
        serializer = PostSerializer(post, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class FeedView(APIView):

    # Returns: Logged-in user's posts, Friends' posts, Ordered by newest first

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # 1- Get accepted friendships
        friendships = Friendship.objects.filter(
            Q(user1=user) | Q(user2=user)
        )

        # 2- Extract friend IDs
        friend_ids = []

        for friendship in friendships:
            if friendship.user1 == user:
                friend_ids.append(friendship.user2.id)
            else:
                friend_ids.append(friendship.user1.id)

        # 3- Fetch posts (own + friends)
        posts = Post.objects.filter(
            Q(author=user) | Q(author__in=friend_ids)
        ).select_related('author').prefetch_related('media').order_by('-created_at')

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)