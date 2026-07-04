from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    AccountSerializer,
    RegisterSerializer
)    
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(
            data=request.data
        )
        if serializer.is_valid():
            user = serializer.save()

            return Response(
                {
                    "message": "User registered successfully",
                    "email": user.email,
                    "full_name": user.full_name,
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class MeView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = AccountSerializer(
            request.user
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

 

    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        refresh_token=request.data.get(
            "refresh"
        )

        if not refresh_token:
            return Response(
                {
                    "error":
                    "Refresh token required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token=RefreshToken(
                refresh_token
            )

            token.blacklist()
            return Response(
                {
                    "message":
                    "Logged out successfully"
                },
                status=status.HTTP_200_OK
            )

        except Exception:
            return Response(
                {
                    "error":
                    "Invalid token"
                },
                status=status.HTTP_401_UNAUTHORIZED
            )


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        if not email:
            return Response(
                {
                    "error": "Email is required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if not password:
            return Response(
                {
                    "error": "Password is required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(
            request,
            email=email,
            password=password
        )

        if user is None:
            return Response(
                {
                    "error": "Invalid credentials"
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            },
            status=status.HTTP_200_OK
        )