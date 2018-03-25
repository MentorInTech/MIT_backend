from rest_framework import serializers
from .models import Program


class ProgramSerializer(serializers.ModelSerializer):

    class Meta:
        model = Program
        fields = ('id', 'title', 'role', 'score')

    def create(self, validated_data):
        return Program.objects.create(**validated_data, profile=self.context['request'].user.profile)

    def update(self, instance, validated_data):
        instance.program_title = validated_data.get('program_title', instance.program_title)
        instance.role = validated_data.get('role', instance.role)
        instance.score = validated_data.get('score', instance.score)
        return instance
