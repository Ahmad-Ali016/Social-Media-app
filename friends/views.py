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


class FriendRequestActionView(APIView):
    # Handles:
    # - Accept (receiver only)
    # - Reject (receiver only)
    # - Cancel/Delete (sender only)

    permission_classes = [IsAuthenticated]

    def patch(self, request, request_id):
        # Get friend request object
        friend_request = get_object_or_404(FriendRequest, id=request_id)

        action = request.data.get("action")

        if action not in ["accept", "reject", "delete"]:
            return Response(
                {"error": "Invalid action."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # if request == ACCEPT
        if action == "accept":
            # Only receiver can accept
            if request.user != friend_request.receiver:
                return Response(
                    {"error": "Only receiver can accept this request."},
                    status=status.HTTP_403_FORBIDDEN
                )

            if friend_request.status != "pending":
                return Response(
                    {"error": "Request is not pending."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Update status
            friend_request.status = "accepted"
            friend_request.save()

            # Normalize order to prevent (B,A) duplication
            user1 = friend_request.sender
            user2 = friend_request.receiver

            if user1.id > user2.id:
                user1, user2 = user2, user1

            Friendship.objects.create(user1=user1, user2=user2)

            return Response(
                {"message": "Friend request accepted."},
                status=status.HTTP_200_OK
            )

        # if request == REJECT
        if action == "reject":
            # Only receiver can reject
            if request.user != friend_request.receiver:
                return Response(
                    {"error": "Only receiver can reject this request."},
                    status=status.HTTP_403_FORBIDDEN
                )

            if friend_request.status != "pending":
                return Response(
                    {"error": "Request is not pending."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            friend_request.status = "rejected"
            friend_request.save()

            return Response(
                {"message": "Friend request rejected."},
                status=status.HTTP_200_OK
            )

        # if request == REJECT/CANCEL
        if action == "reject":
            # Only receiver can reject
            if request.user != friend_request.receiver:
                return Response(
                    {"error": "Only receiver can reject this request."},
                    status=status.HTTP_403_FORBIDDEN
                )

            if friend_request.status != "pending":
                return Response(
                    {"error": "Request is not pending."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            friend_request.status = "rejected"
            friend_request.save()

            return Response(
                {"message": "Friend request rejected."},
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
