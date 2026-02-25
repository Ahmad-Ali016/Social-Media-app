from rest_framework import serializers
from profiles.models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    friend_count = serializers.SerializerMethodField()
    is_friend = serializers.SerializerMethodField()
    is_self = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            'username',
            'bio',
            'profile_picture',
            'friend_count',
            'is_friend',
            'is_self',
            'created_at',
        ]
        read_only_fields = ['created_at']

    def get_friend_count(self, obj):
        from django.db.models import Q
        from friends.models import Friendship

        return Friendship.objects.filter(
            Q(user1=obj.user) | Q(user2=obj.user)
        ).count()

    def get_is_friend(self, obj):
        from django.db.models import Q
        from friends.models import Friendship

        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False

        return Friendship.objects.filter(
            Q(user1=request.user, user2=obj.user) |
            Q(user1=obj.user, user2=request.user)
        ).exists()

    def get_is_self(self, obj):
        request = self.context.get('request')
        return request.user == obj.user if request else False