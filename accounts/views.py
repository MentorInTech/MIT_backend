"""
Copyright (c) 2018， Silicon Valley Career Women.
All rights reserved.
"""
from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ProfileSerializer


class Profile(generics.RetrieveUpdateAPIView):
    """API resource for user profile.

    get:
    Get user profile.

    put:
    Update user profile.
    """
    serializer_class = ProfileSerializer

    def get_object(self):
        user = self.request.user
        return user.profile
