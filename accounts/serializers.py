"""
Copyright (c) 2018， Silicon Valley Career Women.
All rights reserved.
"""
from django.contrib.auth.models import User
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Profile
from programs.serializers import ProgramSerializer


class EmailRequiredUserCreateSerializer(UserCreateSerializer):
    """
    Serializer for User model.

    This only serializes: "id", "username", "email", "password".
    """

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for Profile model."""

    programs = ProgramSerializer(many=True, read_only=True, source='program_set')

    class Meta:
        model = Profile
        fields = ('age_range', 'city', 'state_province', 'job_role', 'job_category',
                  'job_level', 'job_years', 'education_degree', 'education_school',
                  'education_major', 'education_year_graduated', 'interests', 'programs')
        read_only_fields = ('programs',)