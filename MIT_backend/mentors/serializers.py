"""
Copyright (c) 2018， Silicon Valley Career Women.
All rights reserved.
"""
from rest_framework import serializers

from .models import Mentor
from ..accounts.serializers import ProfileSerializer, ProfileWithoutLoginSerializer


class MentorNoLoginSerializer(serializers.ModelSerializer):

    profile = ProfileWithoutLoginSerializer(read_only=True)

    class Meta:
        model = Mentor
        fields = '__all__'
        depth = 2


class MentorWithLoginSerializer(serializers.ModelSerializer):

    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = Mentor
        fields = '__all__'
        depth = 2
