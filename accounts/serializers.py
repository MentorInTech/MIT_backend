from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User

from .models import Profile


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.

    This only serializes: "id", "username", "email", "password".
    """

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        max_length=32,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(min_length=8, write_only=True)

    def create(self, validated_data):
        """Hook to Django's built-in authentication system to create a new User model.

        The regular create method won’t work, so we have to use the create_user method from the User class.
        """
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password'],
        )
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for Profile model."""

    class Meta:
        model = Profile
        fields = ('age_range', 'city', 'state_province', 'job_role', 'job_category',
                  'job_level', 'job_years', 'education_degree', 'education_school',
                  'education_major', 'education_year_graduated', 'interests')
