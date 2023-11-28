# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from base.models import *


class EmployeeLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, attrs):
        user = User.objects.filter(username=attrs.get('username')).first()
        if user and user.check_password(attrs.get('password')):
            refresh = RefreshToken.for_user(user)
            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return data
        raise serializers.ValidationError('Invalid credentials')


class EmployeeProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'
