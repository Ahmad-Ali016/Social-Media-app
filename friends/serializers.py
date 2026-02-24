from rest_framework import serializers
from friends.models import FriendRequest

class IncomingFriendRequestSerializer(serializers.ModelSerializer):
    # Show sender information
    sender_username = serializers.CharField(source='sender.username', read_only=True)
    sender_email = serializers.EmailField(source='sender.email', read_only=True)

    class Meta:
        model = FriendRequest
        fields = [
            'id',
            'sender_username',
            'sender_email',
            'status',
            'created_at',
        ]
