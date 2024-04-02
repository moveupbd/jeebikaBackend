from django.contrib.auth.hashers import make_password

from rest_framework import serializers

from accountio.models import User
from common.choices import UserType
from .models import Employee, License_type, category, company_type, job_post, service_type

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
    user = PublicUserSerializer()

    # Define fields for company_type and license_type as strings
    company_type = serializers.CharField(write_only=True)
    license_type = serializers.CharField(write_only=True)

    class Meta:
        model = Employee
        fields = ['user', 'password', 'confirm_password', 'company_name', 'company_address', 'company_logo', 'website_url', 'company_size', 'company_type', 'id_card_front', 'id_card_back','year_of_eastablishment', 'business_desc', 'license_type', 'license_number', 'license_copy', 'company_owner', 'employee_designation', 'employee_mobile', 'employee_email', 'employee_address']
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

        # Retrieve company_type and license_type from validated data
        company_type_name = validated_data.pop('company_type')
        license_type_name = validated_data.pop('license_type')

        if password != confirm_password:
            raise serializers.ValidationError({"Error": ["Passwords do not match!"]})

        # Get or create company_type and license_type objects
        try:
            company_type_obj = company_type.objects.get(name=company_type_name)
        except:
            raise serializers.ValidationError({"Error": ["Company type does not exist."]})
        
        try:
            license_type_obj = License_type.objects.get(type=license_type_name)
        except :
            raise serializers.ValidationError({"Error": ["License type does not exist."]})

        user = User.objects.create_user(**user_data, password=password, type=UserType.EMPLOYER)
        Employee.objects.create(
            user=user,
            password=make_password(password),
            company_type=company_type_obj,
            license_type=license_type_obj,
            **validated_data
        )
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
    license_type = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ['user', 'company_name', 'company_address', 'company_logo', 'website_url', 'company_size', 'company_type', 'id_card_front', 'id_card_back','year_of_eastablishment', 'business_desc', 'license_type', 'license_number', 'license_copy', 'company_owner', 'employee_designation', 'employee_mobile', 'employee_email', 'employee_address']

    def get_company_type(self, obj):
        return obj.company_type.name if obj.company_type else None

    def get_license_type(self, obj):
        return obj.license_type.type if obj.license_type else None

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
    category = serializers.CharField(write_only=True)
    service_type = serializers.CharField(write_only=True)
    company_type = serializers.CharField(write_only=True)
    user_email = serializers.SerializerMethodField()
    category = serializers.CharField(source='category.name', read_only=True)
    service_type = serializers.CharField(source='service_type.service', read_only=True)
    company_type = serializers.CharField(source='company_type.name', read_only=True)

    class Meta:
        model = job_post
        fields = ['uid', 'user_email', 'category', 'company_name', 'company_type', 'service_type', 'job_designation', 'vacancy', 'department', 'published', 'deadline', 'responsibilities', 'employment_status', 'skill', 'requirements', 'expertise', 'experience', 'location', 'company_info', 'compensation', 'other_facilities', 'apply_procedure']

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




