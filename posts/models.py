from django.db import models
from django.conf import settings

# Create your models here.

class Post(models.Model):

    # Main Post model. A post can contain: Text and Media (PostMedia model)

    VISIBILITY_CHOICES = (
        ('PUBLIC', 'Public'),
        ('FRIENDS', 'Friends'),
        ('PRIVATE', 'Private'),
    )

    # Author of the post
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts'
    )

    # Optional text content
    content = models.TextField(blank=True, null=True)

    # Visibility control
    visibility = models.CharField(
        max_length=10,
        choices=VISIBILITY_CHOICES,
        default='FRIENDS'
    )

    # Timestamp fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']  # Newest posts first

    def __str__(self):
        return f"Post by {self.author.username} ({self.visibility})"

class PostMedia(models.Model):

    # Stores media files (images/videos) related to a Post. Supports multiple media per post (carousel style).

    MEDIA_TYPE_CHOICES = (
        ('IMAGE', 'Image'),
        ('VIDEO', 'Video'),
    )

    # Link media to a post
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='media'
    )

    # Identify whether it's image or video
    media_type = models.CharField(
        max_length=10,
        choices=MEDIA_TYPE_CHOICES
    )

    # Store file (image or video)
    file = models.FileField(
        upload_to='post_media/'
    )

    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']  # Keep original upload order

    def __str__(self):
        return f"{self.media_type} for Post {self.post.id}"

class PostLike(models.Model):

    # Represents a like made by a user on a post. One user can like a post only once.

    post = models.ForeignKey(
        'Post',
        on_delete=models.CASCADE,
        related_name='likes'   # post.likes.all()
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='post_likes'  # user.post_likes.all()
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Prevent duplicate likes
        unique_together = ('post', 'user')

    def __str__(self):
        return f"{self.user.email} liked Post {self.post.id}"

class Comment(models.Model):

    # Flat comment model, single user can comment multiple times on the same post.

    post = models.ForeignKey(
        'Post',
        on_delete=models.CASCADE,
        related_name='comments'
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.author.username} - {self.post.id}"