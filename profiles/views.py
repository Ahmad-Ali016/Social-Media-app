from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from profiles.serializers import ProfileSerializer
from users.models import User


# Create your views here.

class MyProfileView(APIView):
    """
    GET  -> View own profile
    PUT  -> Update full profile
    PATCH -> Partial update profile
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = request.user.profile  # Get logged-in user's profile
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request):
        profile = request.user.profile
        serializer = ProfileSerializer(profile, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        profile = request.user.profile
        serializer = ProfileSerializer(profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    """
    View another user's profile by username
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        profile = user.profile
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)