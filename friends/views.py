from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404
from django.db.models import Q

from users.models import User
from friends.models import Friendship, FriendRequest

# Create your views here.

class SendFriendRequestView(APIView):

    # Allows authenticated user to send a friend request

    permission_classes = [IsAuthenticated]

    def post(self, request, username):
        sender = request.user  # Logged-in user

        # Get receiver user or return 404
        receiver = get_object_or_404(User, username=username)

        # 1- Prevent sending request to yourself
        if sender == receiver:
            return Response(
                {"error": "You cannot send friend request to yourself."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2- Check if already friends
        already_friends = Friendship.objects.filter(
            Q(user1=sender, user2=receiver) |
            Q(user1=receiver, user2=sender)
        ).exists()

        if already_friends:
            return Response(
                {"error": "You are already friends."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 3- Check if friend request already exists (any direction)
        existing_request = FriendRequest.objects.filter(
            Q(sender=sender, receiver=receiver) |
            Q(sender=receiver, receiver=sender)
        ).exists()

        if existing_request:
            return Response(
                {"error": "Friend request already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 4- Create friend request
        FriendRequest.objects.create(
            sender=sender,
            receiver=receiver,
            status='pending'
        )

        return Response(
            {"message": "Friend request sent successfully."},
            status=status.HTTP_201_CREATED
        )