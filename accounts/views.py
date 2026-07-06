from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from .models import User
from accounts.serializers import UserSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
# Create your views here.

class RegisterCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class =RegisterSerializer

class LoginAPIView(APIView):
    authentication_classes=[]
    permission_classes=[]

    def post(self, request):
        username=request.data.get('username')
        password=request.data.get('password')

        if not username or not password:
            return Response({'error':'Username and password is required'},status=status.HTTP_400_BAD_REQUEST)
        
        user=authenticate(
            request=request,
            username=username,
            password=password,
        )
        
        if not user:
            return Response({'error':'Invalid username or password'},status=status.HTTP_401_UNAUTHORIZED)
        
        refresh=RefreshToken.for_user(user)
        access=refresh.access_token

        response=Response({'message':'Login successful'},status=status.HTTP_200_OK)

        response.set_cookie(
            key='access_token',
            value=str(access),
            httponly=True,
            secure=False,
            samesite='lax',
            max_age=60*15,

        )

        response.set_cookie(
            key='refresh_token',
            value=str(refresh),
            httponly=True,
            secure=False,
            samesite='lax',
            max_age=60*60*24*7,
        )

        return response


class RefreshAPIView(APIView):
    authentication_classes=[]
    permission_classes=[]

    def post(self, request):
        refresh_token=request.COOKIES.get('refresh_token')

        if refresh_token is None:
            return Response({'message':'Refresh token is not found'},status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            refresh=RefreshToken(refresh_token)
            access=refresh.access_token

            response=Response({'message':'Token refreshed'},status=status.HTTP_200_OK)
            response.set_cookie(
                key='access_token',
                value=str(access),
                secure=False,
                httponly=True,
                samesite='lax',
                max_age=60*15,
            )
            return response
        except TokenError:
            return Response(
                {
                    "error": "Invalid refresh token."
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
        
    
        

class MeAPIView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self, request):
        serializer=UserSerializer(request.user)
        return Response(serializer.data)

class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        response = Response(
            {
                "message": "Logout successful"
            }
        )
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response


