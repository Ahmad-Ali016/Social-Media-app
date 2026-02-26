from django.urls import path
from posts.views import CreatePostView, FeedView

urlpatterns = [
    path('create/', CreatePostView.as_view(), name='create-post'),
    path('feed/', FeedView.as_view(), name='feed'),
]