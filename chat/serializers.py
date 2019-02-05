from rest_framework import serializers

from dictionary.serializers import DictionarySerializer

from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'username', 'timestamp', 'message')


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    country = serializers.CharField(max_length=2)


class RoomSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    messages = serializers.ListField(
        child=MessageSerializer()
    )
    userlist = serializers.ListField(
        child=UserSerializer()
    )
    dictionary = serializers.ListField(
        child=DictionarySerializer()
    )
