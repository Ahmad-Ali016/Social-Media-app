from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from users.serializers import RegisterSerializer, LoginSerializer


# Create your views here.

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
                },
                "refresh": str(refresh),
                "access": access
            }, status=status.HTTP_200_OK)

        # Return validation errors if credentials invalid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

