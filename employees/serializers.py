from django.contrib.auth.hashers import make_password

from rest_framework import serializers

from accountio.models import User
from common.choices import UserType
from .models import Employee, category, company_type, job_post, service_type

import json 

class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["name", "username", "email", "phone"]
        
    def validate(self, attrs):
        username = attrs.get('username')
        if len(username)<4:
            raise serializers.ValidationError({"Error": ["username must be greated than 4 and less than 12!"]}) # 12 size is fixed in the model
        return attrs

from django.db import IntegrityError

class PublicEmployeeRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    user = serializers.CharField(write_only=True)

    category = serializers.CharField()
    company_type = serializers.CharField(write_only=True)

    class Meta:
        model = Employee
        fields = ['user', 'password', 'confirm_password', 'category', 'company_address', 'company_logo', 'website_url', 'company_size', 'company_type', 'company_subtype', 'id_card_front', 'id_card_back', 'year_of_eastablishment', 'business_desc', 'license_number', 'license_copy', 'representative_name', 'representative_designation', 'representative_mobile', 'representative_email']

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError({"Error": ["Passwords do not match!"]})
        return attrs
    
    def validate_category(self, value):
        try:
            return category.objects.get(name=value)
        except category.DoesNotExist:
            raise serializers.ValidationError("Category does not exist.")

    def create(self, validated_data):
        user_data = json.loads(validated_data.pop('user'))
        password = validated_data.pop('password')
        confirm_password = validated_data.pop('confirm_password')

        company_type_name = validated_data.pop('company_type')

        if password != confirm_password:
            raise serializers.ValidationError({"Error": ["Passwords do not match!"]})

        try:
            company_type_obj = company_type.objects.get(name=company_type_name)
        except:
            raise serializers.ValidationError({"Error": ["Company type does not exist."]})
        
        try:
            user = User.objects.create_user(**user_data, password=password, type=UserType.EMPLOYER)
        except IntegrityError:
            raise serializers.ValidationError({"Error": ["Email or username must be unique."]})
        except ValueError:
            raise serializers.ValidationError({"Error": ["Email or username must be provided."]})
        
        try:
            employee = Employee.objects.create(
                user=user,
                password=make_password(password),
                company_type=company_type_obj,
                **validated_data
            )
        except IntegrityError:
            # Rollback user creation if employee creation fails
            user.delete()
            raise serializers.ValidationError({"Error": ["Email or username must be unique."]})

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
    company_type = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField() 

    class Meta:
        model = Employee
        fields = ['user', 'category', 'company_address', 'company_logo', 'website_url', 'company_size', 'company_type', 'company_subtype', 'id_card_front', 'id_card_back','year_of_eastablishment', 'business_desc', 'license_number', 'license_copy', 'representative_name', 'representative_designation', 'representative_mobile', 'representative_email']

    def get_company_type(self, obj):
        return obj.company_type.name if obj.company_type else None
    
    def get_category(self, obj): 
        return obj.category.name if obj.category else None


    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user_serializer = PrivateUserSerializer(instance.user, data=user_data, partial=True)
            if user_serializer.is_valid():
                user_serializer.save()
            else:
                raise serializers.ValidationError(user_serializer.errors)

        return super().update(instance, validated_data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data
    

class PrivateEmployeePostSerializer(serializers.ModelSerializer):
    category = serializers.CharField()
    service_type = serializers.CharField()
    company_type = serializers.CharField()
    user_email = serializers.SerializerMethodField()

    class Meta:
        model = job_post
        fields = ['uid','user_email', 'company_name', 'category', 'company_type', 'service_type', 'job_designation', 'vacancy', 'department', 'published', 'deadline', 'responsibilities', 'employment_status', 'education', 'education_brief', 'skill', 'requirements', 'expertise', 'experience', 'location', 'company_info','compensation', 'other_facilities', 'apply_procedure', 'source', 'source_prove' ]

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





class PrivateEmployeePostSerializerbyadmin(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=category.objects.all())
    service_type = serializers.PrimaryKeyRelatedField(queryset=service_type.objects.all())
    company_type = serializers.PrimaryKeyRelatedField(queryset=company_type.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    company_name = serializers.CharField(read_only=True)  # Making company_name read-only
    
    class Meta:
        model = job_post
        fields = ['uid', 'user', 'company_name', 'category', 'company_type', 'service_type', 'job_designation', 'vacancy', 'department', 'published', 'deadline', 'responsibilities', 'employment_status', 'skill', 'requirements','expertise', 'experience', 'location', 'company_info','compensation', 'other_facilities', 'apply_procedure' ]

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

    def create(self, validated_data):
        category_instance = validated_data.pop('category')
        service_type_instance = validated_data.pop('service_type')
        company_type_instance = validated_data.pop('company_type')
        
        # Retrieve the user from validated_data
        user = validated_data.get('user')
        
        try:
            # Get the associated Employee and retrieve its company_name
            employee = Employee.objects.get(user=user)
            company_name = employee.company_name
        except Employee.DoesNotExist:
            # Handle the case where no matching Employee instance is found
            # You can raise an error, log a message, or provide a default value for company_name
            company_name = "Zafar Org"
        
        validated_data['category'] = category_instance
        validated_data['service_type'] = service_type_instance
        validated_data['company_type'] = company_type_instance
        validated_data['company_name'] = company_name  # Assign the company_name
        
        return super().create(validated_data)




