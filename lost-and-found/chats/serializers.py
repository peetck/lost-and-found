from rest_framework import serializers

from .models import Message

class MessageSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=255)
    timestamp = serializers.ReadOnlyField()
    seen = serializers.BooleanField()

    def create(self, validated_data):
        return Message.objects.create(**validated_data)