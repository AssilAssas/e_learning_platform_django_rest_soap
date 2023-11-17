from django.shortcuts import render
from django.contrib.auth import get_user_model,logout,login
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response
from .serializers import UserRegisterSerializer,UserLoginSerializer,UserSerializer
from rest_framework import permissions,status 
import re


from .validations import ValidationData
class UserRegister(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user_obj = serializer.save()

            if user_obj:
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)

# views.py

class UserLogin(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = [SessionAuthentication]

    def post(self, request):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        email = data.get('email', '')
        # Validate email and password
        
        if not ValidationData.validate_email(email):
            return Response({"error"}, status=status.HTTP_400_BAD_REQUEST)
        if not ValidationData.validate_password(data.get('password', '')):
            return Response({"error": "Invalid password format"}, status=status.HTTP_400_BAD_REQUEST)
       
        # Continue with serializer validation
        if serializer.is_valid(raise_exception=True):
            user = serializer.check_user(data)
            login(request, user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        
class UserLogout(APIView):
    def get(self,request):
        logout(request)
        return Response(status=status.HTTP_200_OK)
class UserView(APIView):
    def get(self,request):
        user = request.user
        serializer = UserSerializer(user)
        return Response({'user' :serializer.data},status=status.HTTP_200_OK)