from django.shortcuts import render
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate

from rest_framework.generics import get_object_or_404, RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView, CreateAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.filters import SearchFilter
from rest_framework.exceptions import ValidationError

from .serializers import PublicEmployeeRegistrationSerializer, PrivateEmployeeProfileSerializer, PublicEmployeeLoginSerializer, PrivateEmployeePostSerializer
from accountio.models import User
from common.permissions import IsEmployeeUser
from .models import Employee, job_post

from django.http import HttpResponse
from rest_framework_simplejwt.tokens import RefreshToken

class PublicEmployeeRegistrationView(CreateAPIView):
    serializer_class = PublicEmployeeRegistrationSerializer
        

class PublicEmployeeLogin(CreateAPIView):
    serializer_class = PublicEmployeeLoginSerializer

    def generate_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        return access_token, refresh_token
        
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        _email = serializer.validated_data['email']
        _password = serializer.validated_data['password']

        try:
            user = User.objects.get(email__iexact=_email)  # Case-insensitive email comparison

            if not check_password(_password, user.password):
                raise AuthenticationFailed()

            access_token, refresh_token = self.generate_tokens_for_user(user)

            # Set cookies
            response = Response({'tokens': {'access': access_token, 'refresh': refresh_token}, 'status': 'Login successful'}, status=status.HTTP_201_CREATED)
            response.set_cookie('refresh_token', refresh_token, httponly=True)
            
            return response
            
        except User.DoesNotExist:
            raise AuthenticationFailed()

        
        
class PrivateEmployeeProfile(RetrieveUpdateAPIView):
    serializer_class = PrivateEmployeeProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Access the related Employee object of the current user
        employee = self.request.user.employee
        return employee

    def update(self, request, *args, **kwargs):
        # Ensure that only PATCH requests are allowed
        if request.method != 'PATCH':
            return Response({'error': 'Only GET & PATCH method is allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        # Retrieve the Employee object
        instance = self.get_object()
        
        # Serialize the instance with data from the request
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(serializer.data)
    
    
class PrivateEmployeeposts(ListCreateAPIView):
    serializer_class = PrivateEmployeePostSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ["category__name"]
    
    def get_queryset(self):
        user = self.request.user
        return job_post.objects.filter(user=user)

    def perform_create(self, serializer):
        # Automatically set the user field to the authenticated user during creation
        serializer.save(user=self.request.user)


class PrivateEmployeePostDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = PrivateEmployeePostSerializer
    permission_classes = [IsAuthenticated, IsEmployeeUser]

    def get_object(self):
        uid = self.kwargs.get("post_uid")
        if uid is None:
            # Handle the case where `post_uid` is not provided in the URL
            raise ValidationError("Post UID is required.")

        # Filter job_post queryset by UID
        return get_object_or_404(job_post, uid=uid)


    

    
