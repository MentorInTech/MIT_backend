"""
Copyright (c) 2018， Silicon Valley Career Women.
All rights reserved.
"""
from django.contrib.auth.models import User
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Profile


class EmailRequiredUserCreateSerializer(UserCreateSerializer):
    """
    Serializer for User model.

    This only serializes: "id", "username", "email", "password".
    """

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User information"""

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')


class ProfileWithoutLoginSerializer(serializers.ModelSerializer):
    """Serializer for public Profile information"""

    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ('user', 'city', 'state_province', 'job_role', 'job_category',
                  'job_level', 'job_years', 'interests')
        depth = 2


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for full Profile information"""

    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ('user', 'age_range', 'city', 'state_province', 'job_role', 'job_category',
                  'job_level', 'job_years', 'education_degree', 'education_school',
                  'education_major', 'education_year_graduated', 'interests')
        depth = 2
