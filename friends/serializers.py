from rest_framework import serializers
from friends.models import FriendRequest
from users.models import User


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

class FriendListSerializer(serializers.ModelSerializer):

    # Serializer to show basic friend information

    profile_picture = serializers.ImageField(source='profile.profile_picture', read_only=True)
    bio = serializers.CharField(source='profile.bio', read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'profile_picture',
            'bio',
        ]

class UserSerializer(serializers.ModelSerializer):

    # Serializer for User model. Used to expose safe, public user information.

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            # "profile_picture",  # if exists in User model
        ]
        read_only_fields = ["id"]