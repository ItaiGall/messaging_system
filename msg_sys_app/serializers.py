from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Message
        fields = ['id', 'slug', 'owner', 'recipient', 'subject', 'message', 'date_created', 'msg_read']
