from rest_framework import serializers
from authen.models import User 
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str,force_str,smart_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utlis import util
import pdb





class RegisterSerilaizer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=120,min_length=6,write_only=True)
    class Meta:
        model = User
        fields = ['username','email','password']
    def validate(self, attrs):
        email = attrs.get('email','')
        username = attrs.get('username','')
        if not username.isalnum():
            raise serializers.ValidationError('The user name should contains only alphanumeric charcters')
        return attrs
        
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)
    class Meta:
        model = User
        fields = ['token']

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255,min_length=3)
    password = serializers.CharField(max_length=68,min_length=6,write_only=True)
    username = serializers.CharField(max_length=255,min_length=3,read_only=True)
    tokens = serializers.CharField(max_length=255,min_length=3,read_only=True)
    class Meta:
        model = User
        fields = ['email','password','username','tokens']
    def validate(self, attrs):
        email = attrs.get('email','')
        password = attrs.get('password','')
        user = auth.authenticate(email=email,password=password)
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')
        if not user.is_active:
            raise AuthenticationFailed('Account is disabled, Contact admin')
        if not user:
            raise AuthenticationFailed('Invalid credentals, Try again !')
        return {
            'email':user.email,
            'username': user.username,
            'tokens': user.tokens()
        }
        return super().validate(attrs)

class ResetPPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)
    class Meta:
        fields = ['email']