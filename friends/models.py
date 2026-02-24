from django.db import models
from django.conf import settings

# Create your models here.

class FriendRequest(models.Model):

    # Handles pending / accepted / rejected friend requests

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_friend_requests'  # User.sent_friend_requests
    )

    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_friend_requests'  # User.received_friend_requests
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Prevent duplicate friend requests (same sender → receiver)
        unique_together = ('sender', 'receiver')

    def __str__(self):
        return f"{self.sender} → {self.receiver} ({self.status})"

class Friendship(models.Model):

    # Represents accepted friendship between two users

    user1 = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='friendships1'
    )

    user2 = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='friendships2'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Prevent duplicate friendships
        unique_together = ('user1', 'user2')

    def __str__(self):
        return f"{self.user1} ↔ {self.user2}"

FriendRequest.objects.all()