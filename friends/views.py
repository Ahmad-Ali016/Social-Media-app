from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404
from django.db.models import Q

from users.models import User
from friends.models import Friendship, FriendRequest
from friends.serializers import IncomingFriendRequestSerializer, FriendListSerializer

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


class IncomingFriendRequestsView(APIView):
    # Returns all pending friend requests where logged-in user is the receiver

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Get only pending requests where user is receiver
        incoming_requests = FriendRequest.objects.filter(
            receiver=user,
            status='pending'
        ).order_by('-created_at')

        serializer = IncomingFriendRequestSerializer(incoming_requests, many=True)
        return Response(serializer.data)


class AcceptFriendRequestView(APIView):

    # Allows receiver to accept a pending friend request

    permission_classes = [IsAuthenticated]

    def post(self, request, request_id):
        user = request.user

        # Get the friend request or return 404
        friend_request = get_object_or_404(FriendRequest, id=request_id)

        # 1- Ensure logged-in user is the receiver
        if friend_request.receiver != user:
            return Response(
                {"error": "You are not authorized to accept this request."},
                status=status.HTTP_403_FORBIDDEN
            )

        # 2- Ensure request is still pending
        if friend_request.status != 'pending':
            return Response(
                {"error": "This friend request is not pending."},
                status=status.HTTP_400_BAD_REQUEST
            )

        sender = friend_request.sender
        receiver = friend_request.receiver

        # 3- Prevent duplicate friendships (extra safety)
        friendship_exists = Friendship.objects.filter(
            Q(user1=sender, user2=receiver) |
            Q(user1=receiver, user2=sender)
        ).exists()

        if friendship_exists:
            return Response(
                {"error": "Friendship already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 4- Update request status
        friend_request.status = 'accepted'
        friend_request.save()

        # 5- Create Friendship (enforce ordering to prevent duplicates)
        if sender.id < receiver.id:
            user1, user2 = sender, receiver
        else:
            user1, user2 = receiver, sender

        Friendship.objects.create(
            user1=user1,
            user2=user2
        )

        return Response(
            {"message": "Friend request accepted."},
            status=status.HTTP_200_OK
        )

class FriendListView(APIView):

    # Returns all friends of logged-in user

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Get all friendships where user is either user1 or user2
        friendships = Friendship.objects.filter(
            Q(user1=user) | Q(user2=user)
        )

        friends = []

        # Extract the other user from each friendship
        for friendship in friendships:
            if friendship.user1 == user:
                friends.append(friendship.user2)
            else:
                friends.append(friendship.user1)

        friend_serializer = FriendListSerializer(friends, many=True)

        # Serialize logged in user
        user_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }

        return Response({
            "user": user_data,
            "friends": friend_serializer.data
        })
