from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import PersonalProfile, BusinessProfile

User = get_user_model()

class PersonalProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalProfile
        fields = ['first_name', 'last_name', 'professional_title']

class BusinessProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessProfile
        fields = ['business_name', 'registration_number', 'industry', 'business_size']

class UserSerializer(serializers.ModelSerializer):
    personal_profile = PersonalProfileSerializer(required=False)
    business_profile = BusinessProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'city', 'country', 'user_type', 'personal_profile', 'business_profile']
        read_only_fields = ['id']

class PersonalRegistrationSerializer(serializers.ModelSerializer):
    personal_profile = PersonalProfileSerializer()
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'city', 'country', 'user_type', 'password', 'confirm_password', 'personal_profile']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        if data['user_type'] != 'personal':
            raise serializers.ValidationError("User type must be 'personal'.")
        return data

    def create(self, validated_data):
        personal_data = validated_data.pop('personal_profile')
        validated_data.pop('confirm_password')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            phone_number=validated_data.get('phone_number', ''),
            city=validated_data.get('city', ''),
            country=validated_data.get('country', ''),
            user_type=validated_data['user_type'],
            password=validated_data['password']
        )
        PersonalProfile.objects.create(user=user, **personal_data)
        return user

class BusinessRegistrationSerializer(serializers.ModelSerializer):
    business_profile = BusinessProfileSerializer()
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'city', 'country', 'user_type', 'password', 'confirm_password', 'business_profile']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        if data['user_type'] != 'business':
            raise serializers.ValidationError("User type must be 'business'.")
        return data

    def create(self, validated_data):
        business_data = validated_data.pop('business_profile')
        validated_data.pop('confirm_password')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            phone_number=validated_data.get('phone_number', ''),
            city=validated_data.get('city', ''),
            country=validated_data.get('country', ''),
            user_type=validated_data['user_type'],
            password=validated_data['password']
        )
        BusinessProfile.objects.create(user=user, **business_data)
        return user