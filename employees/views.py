from django.http import JsonResponse
from django.contrib.auth.hashers import check_password

from rest_framework.generics import (
    get_object_or_404,
    RetrieveUpdateDestroyAPIView,
    RetrieveUpdateAPIView,
    CreateAPIView,
    ListCreateAPIView,
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from rest_framework.exceptions import ValidationError

from common.permissions import IsEmployeeUser, IsAdminUser
from .models import job_post, Employee

from .serializers import (
    PublicEmployeeRegistrationSerializer,
    PrivateEmployeeProfileSerializer,
    PublicEmployeeLoginSerializer,
    PrivateEmployeePostSerializer,
    PrivateEmployeePostSerializerbyadmin
)

from rest_framework_simplejwt.tokens import RefreshToken


class PublicEmployeeRegistrationView(CreateAPIView):
    serializer_class = PublicEmployeeRegistrationSerializer

    
class PublicEmployeeRegistrationAdminView(CreateAPIView):
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

        _email = serializer.validated_data["email"]
        _password = serializer.validated_data["password"]

        try:
            employee = Employee.objects.get(user__email__iexact=_email)  # Case-insensitive email comparison
            user = employee.user

            if not check_password(_password, user.password):
                raise AuthenticationFailed()

            access_token, refresh_token = self.generate_tokens_for_user(user)

            # Setting the Set-Cookie header
            response = JsonResponse(
                {
                    "tokens": {"access": access_token, "refresh": refresh_token},
                    "status": "Login successful",
                },
                status=status.HTTP_201_CREATED,
            )
            response["Set-Cookie"] = f"access_token = {access_token}; HttpOnly"
            return response

        except Employee.DoesNotExist:
            raise AuthenticationFailed()


class PrivateEmployeeProfile(RetrieveUpdateAPIView):
    serializer_class = PrivateEmployeeProfileSerializer
    permission_classes = [IsAuthenticated, IsEmployeeUser]

    def get_object(self):
        # Access the related Employee object of the current user
        employee = self.request.user.employee
        return employee

    def update(self, request, *args, **kwargs):
        # Ensure that only PATCH requests are allowed
        if request.method != "PATCH":
            return Response(
                {"error": "Only GET & PATCH method is allowed"},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )

        # Retrieve the Employee object
        instance = self.get_object()

        # Serialize the instance with data from the request
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


class PrivateEmployeeposts(ListCreateAPIView):
    serializer_class = PrivateEmployeePostSerializer
    permission_classes = [IsAuthenticated, IsEmployeeUser]
    filter_backends = [SearchFilter]
    search_fields = ["category__name"]

    def get_queryset(self):
        user = self.request.user
        return job_post.objects.filter(user=user)

    def perform_create(self, serializer):
        # Automatically set the user field to the authenticated user during creation
        serializer.save(user=self.request.user)

class PrivateEmployeepostsByadmin(ListCreateAPIView):
    serializer_class = PrivateEmployeePostSerializerbyadmin
    permission_classes = [IsAuthenticated, IsAdminUser]
    filter_backends = [SearchFilter]
    search_fields = ["category__name"]

    def get_queryset(self):
        # Return the queryset based on the currently authenticated user
        return job_post.objects.all().order_by('-updated_at')[:5]

    def perform_create(self, serializer):
        # Retrieve the selected user ID from the request data
        selected_user_id = self.request.data.get('user')
        
        # Pass the selected user ID to the serializer
        serializer.save(user_id=selected_user_id)


class PrivateEmployeePostDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = PrivateEmployeePostSerializer
    permission_classes = [IsAuthenticated, IsEmployeeUser]

    def get_queryset(self):
        return job_post.objects.all()

    def get_object(self):
        uid = self.kwargs.get("post_uid")
        if uid is None:
            # Handle the case where `post_uid` is not provided in the URL
            raise ValidationError("Post UID is required.")

        # Filter job_post queryset by UID
        return get_object_or_404(job_post, uid=uid)
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Successfully deleted the post."}, status=status.HTTP_204_NO_CONTENT)
