from rest_framework import serializers
from .models import Goal


class GoalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Goal
        fields = ('program_title', 'role', 'score')

    def create(self, validated_data):
        return Goal(**validated_data)

    def update(self, instance, validated_data):
        instance.program_title = validated_data.get('program_title', instance.program_title)
        instance.role = validated_data.get('role', instance.role)
        instance.score = validated_data.get('score', instance.score)
        return instance