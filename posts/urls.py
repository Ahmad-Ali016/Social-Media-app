from django.urls import path
from posts.views import CreatePostView, FeedView, PostLikeView

urlpatterns = [
    path('create/', CreatePostView.as_view(), name='create-post'),
    path('feed/', FeedView.as_view(), name='feed'),
    path('like/<int:post_id>/', PostLikeView.as_view(), name='post-like'),
]