"""
Copyright (c) 2018， Silicon Valley Career Women.
All rights reserved.
"""
from rest_framework import serializers

from .models import Program


class ProgramSerializer(serializers.ModelSerializer):
    started = serializers.DateTimeField(required=False, allow_null=True)
    ended = serializers.DateTimeField(required=False, allow_null=True)
    next_sync_up_time = serializers.DateTimeField(required=False, allow_null=True)

    class Meta:
        model = Program
        fields = (
            'id', 'title', 'mentor', 'mentee', 'score', 'goal', 'started', 'ended', 'last_updated', 'next_sync_up_time')
        read_only_fields = ('mentee', 'last_updated')

    def create(self, validated_data):
        return Program.objects.create(**validated_data, mentee=self.context['request'].user)
