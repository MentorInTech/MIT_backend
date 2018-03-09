from rest_framework import serializers
from .models import Goal


class GoalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Goal
        fields = ('program_title', 'role', 'score')
