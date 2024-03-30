from django.contrib.auth.hashers import make_password

from rest_framework import serializers

from accountio.models import User
from common.choices import UserType
from .models import Employee, category, company_type, job_post, service_type

class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["name", "username", "email", "phone"]
        
    def validate(self, attrs):
        username = attrs.get('username')
        if len(username)<4:
            raise serializers.ValidationError({"Error": ["username must be greated than 4 and less than 12!"]}) # 12 size is fixed in the model
        return attrs

class PublicEmployeeRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    user = PublicUserSerializer()  # Assuming you have defined PublicUserSerializer

    class Meta:
        model = Employee
        fields = ['user', 'password', 'confirm_password', 'company_name', 'company_address', 'company_logo', 'website_url', 'company_size', 'industry_type', 'id_card_front', 'id_card_back','year_of_eastablishment', 'business_desc', 'license_type', 'license_number', 'license_copy', 'company_owner', 'employee_designation', 'employee_mobile', 'employee_email', 'employee_address']
        extra_kwargs = {
            'password': {'write_only': True}
        }

        def validate(self, attrs):
            password = attrs.get('password')
            confirm_password = attrs.get('confirm_password')
            if password != confirm_password:
                raise serializers.ValidationError({"Error": ["Passwords do not match!"]})
            return attrs


    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = validated_data.pop('password')
        confirm_password = validated_data.pop('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError({"Error": ["Passwords do not match!"]})
        user = User.objects.create_user(**user_data, password=password, type=UserType.EMPLOYER)
        Employee.objects.create(user=user,password=make_password(password), **validated_data)
        return user

    def to_representation(self, instance):
        payload = {"message": f"Registration successful for {instance.username}."}
        return payload

    

class PublicEmployeeLoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(max_length=228)
    class Meta:
        model = User
        fields = ["email", "password"]
        
class PrivateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','username','name', 'phone', 'type']
    
class PrivateEmployeeProfileSerializer(serializers.ModelSerializer):
    user = PrivateUserSerializer()

    class Meta:
        model = Employee
        fields = ['user', 'company_name', 'company_address', 'company_logo', 'website_url', 'company_size', 'industry_type', 'id_card_front', 'id_card_back','year_of_eastablishment', 'business_desc', 'license_type', 'license_number', 'license_copy', 'company_owner', 'employee_designation', 'employee_mobile', 'employee_email', 'employee_address']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user_serializer = PrivateUserSerializer(instance.user, data=user_data, partial=True)
            if user_serializer.is_valid():
                user_serializer.save()
            else:
                raise serializers.ValidationError(user_serializer.errors)

        return super().update(instance, validated_data)


class PrivateEmployeePostSerializer(serializers.ModelSerializer):
    category = serializers.CharField(write_only=True)
    service_type = serializers.CharField(write_only=True)
    company_type = serializers.CharField(write_only=True)
    user_email = serializers.SerializerMethodField()

    class Meta:
        model = job_post
        fields = ['uid','user_email', 'company_title', 'category', 'company_type', 'service_type', 'job_designation', 'vacancy', 'department', 'published', 'deadline', 'responsibilities', 'employment_status', 'skill', 'requirements','expertise', 'experience', 'location', 'company_info','compensation', 'other_facilities', 'apply_procedure' ]

    def get_user_email(self, obj):
        return obj.user.email 
    
    def validate_category(self, value):
        try:
            return category.objects.get(name=value)
        except category.DoesNotExist:
            raise serializers.ValidationError("Category does not exist.")

    def validate_service_type(self, value):
        try:
            return service_type.objects.get(service=value)
        except service_type.DoesNotExist:
            raise serializers.ValidationError("Service type does not exist.")
    def validate_company_type(self, value):
        try:
            return company_type.objects.get(name=value)
        except company_type.DoesNotExist:
            raise serializers.ValidationError("Company type does not exist.")

    def create(self, validated_data):
        category_instance = validated_data.pop('category')
        service_type_instance = validated_data.pop('service_type')
        company_type_instance = validated_data.pop('company_type')
        validated_data['category'] = category_instance
        validated_data['service_type'] = service_type_instance
        validated_data['company_type'] = company_type_instance
        return super().create(validated_data)