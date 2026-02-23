from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from users.serializers import RegisterSerializer, LoginSerializer, UserListSerializer
from django.contrib.auth import get_user_model

# Create your views here.

User = get_user_model()

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Generate JWT token
            refresh = RefreshToken.for_user(user)
            return Response({
                "user": serializer.data,
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']

            # Mark user as logged in
            user.is_log_in = True
            user.save(update_fields=['is_log_in'])

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access = str(refresh.access_token)

            return Response({
                "user": {
                    "email": user.email,
                    "username": user.username,
                    "bio": user.bio,
                    "gender": user.gender,
                    "profile_picture": user.profile_picture.url if user.profile_picture else None,
                    "is_log_in": user.is_log_in,
                },
                "refresh": str(refresh),
                "access": access
            }, status=status.HTTP_200_OK)

        # Return validation errors if credentials invalid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserListView(APIView):
    permission_classes = [permissions.IsAdminUser]  # Only staff users can access

    def get(self, request):
        # Get all users
        users = User.objects.all()
        serializer = UserListSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
