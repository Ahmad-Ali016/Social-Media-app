from django.urls import path
from posts.views import CreatePostView, FeedView, PostLikeView, CreateCommentView

urlpatterns = [
    path('create/', CreatePostView.as_view(), name='create-post'),
    path('feed/', FeedView.as_view(), name='feed'),
    path('like/<int:post_id>/', PostLikeView.as_view(), name='post-like'),
    path('comment/<int:post_id>/', CreateCommentView.as_view(), name='post-comment  '),
]