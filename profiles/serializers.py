from rest_framework import serializers
from profiles.models import Profile



class ProfileSerializer(serializers.ModelSerializer):
    # Show some user info inside profile response
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Profile
        fields = [
            'username',
            'email',
            'bio',
            'profile_picture',
            'created_at',
        ]
        read_only_fields = ['created_at']