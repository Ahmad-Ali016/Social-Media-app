from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from profiles.serializers import ProfileSerializer
from users.models import User

# Create your views here.

class MyProfileView(APIView):

    # GET  -> View own profile
    # PUT  -> Update full profile
    # PATCH -> Partial update profile

    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get logged-in user's profile
        profile = request.user.profile

        # Pass request inside context (important for computed fields)
        serializer = ProfileSerializer(
            profile,
            context={'request': request}
        )
        return Response(serializer.data)

    def put(self, request):
        # Full update of profile
        profile = request.user.profile

        serializer = ProfileSerializer(
            profile,
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        # Partial update of profile
        profile = request.user.profile

        serializer = ProfileSerializer(
            profile,
            data=request.data,
            partial=True,  # Allows partial update
            context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):

    """ GET -> View another user's profile by username """

    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        # Get user by username or return 404
        user = get_object_or_404(User, username=username)

        # Get that user's profile
        profile = user.profile

        # Pass request context for friend detection, self-check, etc.
        serializer = ProfileSerializer(
            profile,
            context={'request': request}
        )

        return Response(serializer.data)